from django.db import models
from django.conf import settings
from astrochallenge.objects.models import AstroObject, SolarSystemObject
from astrochallenge.accounts.models import UserProfile


class Challenge(models.Model):
    target = models.CharField(max_length=200, choices=settings.CHALLENGE_TYPES)
    type = models.CharField(max_length=200, choices=(('set', 'set'), ('numeric', 'numeric')))
    solarsystemobjects = models.ManyToManyField(SolarSystemObject, null=True, blank=True)
    astroobjects = models.ManyToManyField(AstroObject, null=True, blank=True)
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=1)
    multiplier = models.IntegerField(default=1)
    bonus = models.IntegerField(default=0)
    complete_bonus = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to="challenges", blank=True, null=True)

    def __unicode__(self):
        return self.name


class CompletedChallenge(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    challenge = models.ForeignKey(Challenge)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'challenge')

    def __unicode__(self):
        return "{0}-{1}-{2}".format(str(self.user_profile), str(self.challenge), str(self.date))
