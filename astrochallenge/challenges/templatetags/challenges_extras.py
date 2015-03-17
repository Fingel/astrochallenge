from django import template

from astrochallenge.challenges.models import CompletedChallenge

register = template.Library()


@register.filter
def has_completed_challenge(user, challenge):
    return True if CompletedChallenge.objects.filter(user_profile=user.userprofile, challenge=challenge).exists() else False
