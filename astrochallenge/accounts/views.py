from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {"name": "austin"}
    return render(request, 'accounts/index.html', context)
