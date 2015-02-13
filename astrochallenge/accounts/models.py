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
    lat = models.DecimalField("latitude", max_digits=10, decimal_places=7, blank=True, null=True)
    lng = models.DecimalField("longitude", max_digits=10, decimal_places=7, blank=True, null=True)
    profile_text = models.TextField(blank=True, default="")

    @property
    def observer(self):
        observer = ephem.Observer()
        observer.lat, observer.lon, observer.date = str(self.lat), str(self.lng), timezone.localtime(timezone.now(), self.timezone)
        return observer

    @property
    def sunset(self):
        sun = ephem.Sun()
        sun.compute(self.observer)
        return timezone.make_aware(self.observer.next_setting(sun).datetime(), pytz.UTC)


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        instance.userprofile
    except:
        UserProfile(user=instance).save()
