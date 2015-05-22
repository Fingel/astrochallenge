from django import template
from astrochallenge.accounts.models import Kudos

register = template.Library()


@register.filter
def has_kudoed(user, observation):
    return Kudos.objects.filter(user_profile=user.userprofile,
                                observation=observation).exists()
