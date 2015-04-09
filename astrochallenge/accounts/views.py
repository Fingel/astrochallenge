from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import mail_admins, EmailMessage
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import logging
import datetime

from astro_comments.models import CustomComment
from astrochallenge.objects.models import Observation
from astrochallenge.accounts.models import Equipment, UserProfile, Kudos
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
        for challenge in Challenge.current_challenges():
            if not CompletedChallenge.objects.filter(user_profile=request.user.userprofile, challenge=challenge).exists():
                next_challenge = challenge
                break
    else:
        next_challenge = Challenge.current_challenges().first()

    #  TODO: Change make this much more effecient
    userprofiles = UserProfile.objects.all().exclude(observation=None)
    leaderboard = list(sorted(userprofiles, key=lambda userprofile: userprofile.points, reverse=True))
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
    anchor = ""
    kudos = 0
    observations = Observation.objects.filter(user_profile=member.userprofile)
    for observation in observations:
        kudos += observation.kudos_set.count()
    form = ObservationLogForm()
    if request.method == "POST":
        form = ObservationLogForm(request.POST)
        anchor = "#tab_observations"
        if form.is_valid():
            start_time = form.cleaned_data['start_time'] if form.cleaned_data['start_time'] else datetime.date(1900, 1, 1)
            end_time = form.cleaned_data['end_time'] if form.cleaned_data['end_time'] else datetime.date(2999, 1, 1)
            observations = Observation.objects.filter(user_profile=member.userprofile,
                date__gte=start_time,
                date__lte=end_time)
        else:
            messages.error(request, "Invalid date range")
    challenges = [completed_challenge.challenge for completed_challenge in member.userprofile.completedchallenge_set.all()]
    return render(request, 'accounts/profile.html', {'member': member,
                                                    'challenges': challenges,
                                                    'observations': observations,
                                                    'form': form,
                                                    'anchor': anchor,
                                                    'kudos': kudos})


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
                logger.info('{0} WILL SEND EMAIL: Dest: {1}'.format(datetime.datetime.now(), ob.user_profile.user.email))
                try:
                    observation = kudos.observation
                    from_user = kudos.user_profile.user
                    text = get_template('accounts/mail/kudos.txt')
                    context = Context({'from_user': from_user.username, 'observation': observation})
                    message = text.render(context)
                    subject = "{0} gave you kudos on your observation!".format(from_user.username)
                    to = (observation.user_profile.user.email,)
                    email = EmailMessage(subject=subject, body=message, to=to)
                    logger.info('{0} EMAIL PREPARE: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
                    email.send()
                    logger.info('{0} EMAIL SENT: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
                except Exception as exception:
                    logger.error('{0} EMAIL - EXCEPTION: Subject: {1} Dest: {2} {3}'.format(datetime.datetime.now(), subject, to, str(exception)))

                # class KudosThread(threading.Thread):
                #     def __init__(self, kudos, **kwargs):
                #         self.kudos = kudos
                #         super(KudosThread, self).__init__(**kwargs)

                #     def run(self):
                #         try:
                #             observation = self.kudos.observation
                #             from_user = self.kudos.user_profile.user
                #             text = get_template('accounts/mail/kudos.txt')
                #             context = Context({'from_user': from_user.username, 'observation': observation})
                #             message = text.render(context)
                #             subject = "{0} gave you kudos on your observation!".format(from_user.username)
                #             to = (observation.user_profile.user.email,)
                #             email = EmailMessage(subject=subject, body=message, to=to)
                #             logger.info('{0} EMAIL PREPARE: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
                #             email.send()
                #             logger.info('{0} EMAIL SENT: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
                #         except Exception as exception:
                #             logger.error('{0} EMAIL - EXCEPTION: Subject: {1} Dest: {2} {3}'.format(datetime.datetime.now(), subject, to, str(exception)))

                # KudosThread(kudos).start()
        return JsonResponse({'result': 'success', 'kudos': len(ob.kudos_set.all())})


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
