from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

from astrochallenge.objects.models import Observation
from forms import UserForm, ProfileForm


def index(request):
    observations = Observation.objects.all()

    context = {
        "observations": observations,
        "time": timezone.now(),
    }
    return render(request, 'accounts/index.html', context)


def member_profile(request, username):
    member = get_object_or_404(User, username=username)
    return render(request, 'accounts/memberprofile.html', {'member': member})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})


@login_required
def edit_profile(request):
    if request.method == 'GET':
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/profile_form.html', context)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            del(request.session['django_timezone'])
            messages.success(request, "Profile sucessfully updated")
            return redirect('profile')
        else:
            messages.error(request, 'There was an error with the form')
            return render(request, 'accounts/profile_form.html', {'user_form': user_form, 'profile_form': profile_form})
