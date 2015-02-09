from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from models import UserProfile
from forms import UserForm, ProfileForm


def index(request):
    context = {"name": "austin"}
    return render(request, 'accounts/index.html', context)


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
            messages.success(request, "Profile sucessfully updated")
            return redirect('profile')
        else:
            messages.error(request, 'There was an error with the form')
            return render(request, 'accounts/profile_form.html', {'user_form': user_form, 'profile_form': profile_form})

