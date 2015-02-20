from django import template

register = template.Library()


@register.filter
def has_observed(user, object):
    return object.observations.filter(user_profile__user__username=user.username).exists()


@register.filter
def last_observation(user, object):
    return object.observations.filter(user_profile__user__username=user.username).first()


@register.filter
def first_observation(user, object):
    return object.observations.filter(user_profile__user__username=user.username).last()


@register.filter
def show_username(user):
    return user.username
