from django import template

from astrochallenge.challenges.models import CompletedChallenge

register = template.Library()


@register.filter
def has_completed_challenge(user, challenge):
    return True if CompletedChallenge.objects.filter(user_profile=user.userprofile, challenge=challenge).exists() else False


@register.filter
def rating_stars(rating):
    html = ""
    for i in range(0, rating):
        html += '<span class="glyphicon glyphicon-star"></span>'
    for i in range(0, 5 - rating):
        html += '<span class="glyphicon glyphicon-star-empty"></span>'
    return html
