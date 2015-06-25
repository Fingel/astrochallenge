from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import logging
import datetime

from astro_comments.models import CustomComment
from astrochallenge.objects.models import Observation, SolarSystemObject, Supernova, AstroObject
from astrochallenge.accounts.models import Equipment, UserProfile, Kudos
from astrochallenge.accounts.tasks import email_task
from astrochallenge.objects.utils import moon_phase
from astrochallenge.challenges.models import Challenge, CompletedChallenge
from forms import UserForm, ProfileForm, EquipmentForm, ContactForm, ObservationLogForm


logger = logging.getLogger(settings.DEFAULT_LOGGER)


def index(request):
    observations = Observation.objects.all()
    comments = CustomComment.objects.all()[:5]
    percentage, name, letter = moon_phase(timezone.now())
    next_challenge = None
    if request.user.is_authenticated():
        for challenge in Challenge.current_challenges().exclude(type='numeric'):
            if not CompletedChallenge.objects.filter(user_profile=request.user.userprofile, challenge=challenge).exists():
                next_challenge = challenge
                break
    else:
        next_challenge = Challenge.current_challenges().exclude(type='numeric').first()

    #  TODO: Change make this much more effecient
    userprofiles = UserProfile.objects.all().exclude(observation=None)
    leaderboard = list(sorted(userprofiles, key=lambda userprofile: userprofile.points, reverse=True))
    latest_comet = SolarSystemObject.objects.filter(type='C').order_by('-date_added')[0]
    supernova = Supernova.brightest_supernova()
    popular_dso = AstroObject.objects.annotate(Count('observations')).order_by('-observations__count')[:5]
    popular_sso = SolarSystemObject.objects.annotate(Count('observations')).order_by('-observations__count')[:5]
    context = {
        "comments": comments,
        "observations": observations,
        "moon_percentage": percentage,
        "moon_name": name,
        "moon_letter": letter,
        "time": timezone.now(),
        "next_challenge": next_challenge,
        "leaderboard": leaderboard,
        "latest_comet": latest_comet,
        "supernova": supernova,
        "popular_dso": popular_dso,
        "popular_sso": popular_sso,
    }
    return render(request, 'accounts/index.html', context)


def profile(request, username=None):
    if not username:
        if request.user.is_authenticated():
            member = request.user
        else:
            return redirect('auth_login')
    else:
        member = get_object_or_404(User, username=username)
    anchor = ""
    kudos = 0
    observations = Observation.objects.filter(user_profile=member.userprofile)
    featured_observations = []
    for observation in observations:
        kudos += observation.kudos_set.count()
        if observation.featured:
            featured_observations.append(observation)

    form = ObservationLogForm()
    if request.GET.get('start_time'):
        form = ObservationLogForm(request.GET)
        anchor = "#tab_observations"
        if form.is_valid():
            start_time = form.cleaned_data['start_time'] if form.cleaned_data['start_time'] else datetime.date(1900, 1, 1)
            end_time = form.cleaned_data['end_time'] if form.cleaned_data['end_time'] else datetime.date(2999, 1, 1)
            observations = Observation.objects.filter(user_profile=member.userprofile,
                date__gte=start_time,
                date__lte=end_time).order_by('date')
        else:
            messages.error(request, "Invalid date range")
    challenges = [completed_challenge.challenge for completed_challenge in member.userprofile.completedchallenge_set.all()]
    return render(request, 'accounts/profile.html', {'member': member,
                                                    'challenges': challenges,
                                                    'observations': observations,
                                                    'form': form,
                                                    'anchor': anchor,
                                                    'kudos': kudos,
                                                    'featured_observations': featured_observations[:6]})


@login_required
@require_POST
@csrf_exempt
def add_equipment(request):
    instrument = request.POST['instrument']
    if len(instrument) > 0:
        equipment = Equipment(
            instrument=instrument,
            user_profile=request.user.userprofile
        )
        equipment.save()
        return JsonResponse({
            'result': 'success',
            'equipment': {
                'id': equipment.id,
                'instrument': equipment.instrument
            }
        })
    else:
        return JsonResponse({'result': 'error'})


@require_GET
def give_kudos(request, observation):
    if not request.user.is_authenticated():
        return JsonResponse({'result': 'error', 'redirect': '/accounts/login/'})
    else:
        ob = get_object_or_404(Observation, pk=observation)
        if ob.user_profile == request.user.userprofile:
            return JsonResponse({'result': 'error', 'msg': 'You can\'t give yourself kudos!'})
        if not Kudos.objects.filter(user_profile=request.user.userprofile, observation=ob).exists():
            kudos = Kudos(user_profile=request.user.userprofile, observation=ob)
            kudos.save()
            if ob.user_profile.recieve_notification_emails:
                text = get_template('accounts/mail/kudos.txt')
                context = Context(
                    {'from_user': kudos.user_profile.user.username,
                     'observation': kudos.observation}
                )
                body = text.render(context)
                subject = "{0} gave you kudos on your observation!".format(
                    kudos.user_profile.user.username
                )
                to = (kudos.observation.user_profile.user.email,)
                email_task.delay(subject=subject, body=body, to=to)
        return JsonResponse({'result': 'success', 'kudos': len(ob.kudos_set.all())})


@login_required
@require_GET
def list_equipment(request):
    if not request.user.is_authenticated():
        return JsonResponse({'result': 'error', 'redirect': '/accounts/login/'})
    else:
        equipment = []
        for e in request.user.userprofile.equipment_set.all():
            equipment.append({'id': e.id, 'instrument': e.instrument})
        return JsonResponse({'equipment': equipment})


@login_required
@require_GET
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, user_profile=request.user.userprofile)
    equipment.delete()
    return JsonResponse({'result': 'success'})


@login_required
@require_GET
def delete_comment(request, pk):
    comment = get_object_or_404(CustomComment, pk=pk, user=request.user)
    comment.delete()
    return redirect(comment.content_object.get_absolute_url() + '#tab_discussion')


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
