from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View

from astro_comments.models import CustomComment
from astrochallenge.objects.models import Observation
from astrochallenge.accounts.models import Equipment, UserProfile
from astrochallenge.objects.utils import moon_phase
from astrochallenge.challenges.models import Challenge, CompletedChallenge
from forms import UserForm, ProfileForm, EquipmentForm, ContactForm


def index(request):
    observations = Observation.objects.all()
    comments = CustomComment.objects.all()[:5]
    percentage, name, letter = moon_phase(timezone.now())
    next_challenge = None
    if request.user.is_authenticated():
        for challenge in Challenge.current_challenges():
            if not CompletedChallenge.objects.filter(user_profile=request.user.userprofile, challenge=challenge).exists():
                next_challenge = challenge
                break
    else:
        next_challenge = Challenge.current_challenges().first()

    #  TODO: Change make this much more effecient
    userprofiles = UserProfile.objects.all().exclude(observation=None)
    leaderboard = list(reversed(sorted(userprofiles, key=lambda userprofile: userprofile.points)))
    context = {
        "comments": comments,
        "observations": observations,
        "moon_percentage": percentage,
        "moon_name": name,
        "moon_letter": letter,
        "time": timezone.now(),
        "next_challenge": next_challenge,
        "leaderboard": leaderboard,
    }
    return render(request, 'accounts/index.html', context)


def profile(request, username):
    member = get_object_or_404(User, username=username)
    challenges = [completed_challenge.challenge for completed_challenge in member.userprofile.completedchallenge_set.all()]
    return render(request, 'accounts/profile.html', {'member': member, 'challenges': challenges})


@login_required
@require_POST
def add_equipment(request):
    equipment_form = EquipmentForm(request.POST)
    if equipment_form.is_valid():
        equipment = equipment_form.save(commit=False)
        equipment.user_profile = request.user.userprofile
        equipment.save()
        messages.success(request, "Equipment added")
    else:
        messages.error(request, "There was an error with your submission")
    return redirect('edit-profile')


@login_required
@require_GET
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, user_profile=request.user.userprofile)
    equipment.delete()
    messages.success(request, "Equipment deleted.")
    return redirect('edit-profile')


@login_required
def edit_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'GET':
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.userprofile)
        equipment_form = EquipmentForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'equipment_form': equipment_form,
        }
        return render(request, 'accounts/profile_form.html', context)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.userprofile)
        equipment_form = EquipmentForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            del(request.session['django_timezone'])
            messages.success(request, "Profile sucessfully updated")
            return redirect('profile', username=user.username)
        else:
            return render(request, 'accounts/profile_form.html', {'user_form': user_form, 'profile_form': profile_form, 'equipment_form': equipment_form})


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'accounts/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Looks like your captcha was wrong!")
            return render(request, 'accounts/contact.html', {'form': form})
        else:
            mail_admins(
                "New contact form submission from {0}".format(form.cleaned_data['email']),
                form.cleaned_data["feedback"],
                )
            messages.success(request, "Thank you! We'll get back to you as soon as possible.")
            return render(request, 'accounts/contact.html', {'form': ContactForm()})
