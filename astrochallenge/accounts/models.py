import pytz
import ephem
from django.db import models
from django.db.models import Sum
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
    recieve_notification_emails = models.BooleanField(default=True, help_text="Recieve emails when someone gives you kudos or comments on your observations.")

    def __unicode__(self):
        return self.user.username

    @property
    def points(self):
        points = 0
        ob_points = self.observation_set.all().aggregate(
            Sum('points_earned')
        ).get('points_earned__sum', 0)
        challenge_points = self.completedchallenge_set.all().aggregate(
            Sum('challenge__complete_bonus')
        ).get('challenge__complete_bonus__sum', 0)
        if ob_points:
            points = points + ob_points
        if challenge_points:
            points = points + challenge_points
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


class Kudos(models.Model):
    observation = models.ForeignKey('objects.Observation')
    user_profile = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} on {1}".format(self.user_profile.user.username, self.observation)


#  Initial account setup
@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        instance.userprofile
    except:
        up = UserProfile(user=instance)
        up.save()
        Equipment(instrument="Naked eye", user_profile=up).save()
