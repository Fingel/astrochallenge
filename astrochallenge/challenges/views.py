from django.views.generic.list import ListView

from models import Challenge


class ChallengeListView(ListView):
    def get_queryset(self):
        return Challenge.current_challenges()
