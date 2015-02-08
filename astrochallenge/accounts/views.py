from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from models import UserProfile
from forms import ProfileForm


def index(request):
    context = {"name": "austin"}
    return render(request, 'accounts/index.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})


@login_required
def edit_profile(request):
    if request.method == 'GET':
        form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'accounts/profile_form.html', {'form': form})
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            messages.error(request, 'There was an error with the form')
            return render(request, 'accounts/profile_form.html', {'form': form})

