from django import template

register = template.Library()


@register.filter
def mass_unicode(mass_unit):
    if mass_unit == 'e':
        return u'\u2295'
    if mass_unit == 's':
        return u'\u2609'
    if mass_unit == 'j':
        return "<sub>j</sub>"
    return ""


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
