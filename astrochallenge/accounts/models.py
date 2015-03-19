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
    location = models.CharField(max_length=200, blank=True, default="", help_text="Doesn't need to be accurate, just a description of your location. e.g \"San Francisco\"")
    lat = models.FloatField("latitude", default=0.0, help_text="The latitude form which you most often observe from.")
    lng = models.FloatField("longitude", default=0.0, help_text="The longitude from which you most often observe from.")
    elevation = models.IntegerField(default=0, help_text="The elevation, in meters, from which you most often observe from.")
    profile_text = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.user.username

    @property
    def points(self):
        points = 0
        for observation in self.observation_set.all():
            points += observation.points_earned
        for completed_challenge in self.completedchallenge_set.all():
            points += completed_challenge.challenge.complete_bonus
        return points

    @property
    def observer(self):
        observer = ephem.Observer()
        observer.lat, observer.lon, observer.elevation = str(self.lat), str(self.lng), self.elevation
        return observer

    @property
    def sunset(self):
        try:
            sun = ephem.Sun()
            sun.compute(self.observer)
            return timezone.make_aware(self.observer.next_setting(sun).datetime(), pytz.UTC)
        except:
            return "No Set/No Rise!"


class Equipment(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    instrument = models.CharField(max_length=200)

    @property
    def observation_count(self):
        Observation = models.get_model('objects', 'Observation')
        return Observation.objects.filter(equipment=self).count()

    def __unicode__(self):
        return self.instrument


#  Initial account setup
@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        instance.userprofile
    except:
        up = UserProfile(user=instance)
        up.save()
        Equipment(instrument="Naked eye", user_profile=up).save()
