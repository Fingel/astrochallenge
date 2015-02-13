import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if not tzname:
            if request.user.is_authenticated():
                tzname = request.user.userprofile.timezone.zone
                request.session['django_timezone'] = tzname
            else:
                tzname = 'UTC'
        timezone.activate(pytz.timezone(tzname))
