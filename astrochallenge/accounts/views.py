from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    context = {"name": "austin"}
    return render(request, 'accounts/index.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})
