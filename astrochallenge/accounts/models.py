import pytz
import ephem
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    timezone = TimeZoneField(default="UTC")
    location = models.CharField(max_length=200, blank=True, default="")
    lat = models.FloatField("latitude", default=0.0)
    lng = models.FloatField("longitude", default=0.0)
    profile_text = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.user.username

    @property
    def observer(self):
        observer = ephem.Observer()
        observer.lat, observer.lon = str(self.lat), str(self.lng)
        return observer

    @property
    def sunset(self):
        sun = ephem.Sun()
        sun.compute(self.observer)
        return timezone.make_aware(self.observer.next_setting(sun).datetime(), pytz.UTC)

    def az_alt_for_object(self, object):
        object = object.fixed_body
        object.compute(self.observer)
        return (str(object.az), str(object.alt))


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        instance.userprofile
    except:
        UserProfile(user=instance).save()
