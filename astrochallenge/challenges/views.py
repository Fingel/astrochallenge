from django.views.generic.list import ListView
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse

from models import Challenge
from utils import SigImage


class ChallengeListView(ListView):
    def get_queryset(self):
        return Challenge.current_challenges()


class SigImageView(View):
    def get(self, request):
        user_id = request.GET.get('user')
        challenge_ids = request.GET.get('challenges')
        inverted = request.GET.get('inverted', False)
        if not user_id or not challenge_ids:
            raise Http404("You must supply user and challenges parameteres")

        user = get_object_or_404(User, pk=user_id)
        challenges = []
        for challenge_id in challenge_ids.split(','):
            challenges.append(get_object_or_404(Challenge, pk=challenge_id))

        sig = SigImage(user, challenges, inverted)
        image = sig.draw()
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response


def challenge_list_json(request):
    challenges = []
    for challenge in Challenge.current_challenges():
        challenges.append({'id': challenge.id,
                           'name': challenge.name,
                           'short_name': challenge.short_name})
    return JsonResponse({'challenges': challenges})
