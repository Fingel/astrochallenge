from django.db import models
from django.conf import settings
from django.core import urlresolvers

from astrochallenge.objects.models import AstroObject, SolarSystemObject
from astrochallenge.accounts.models import UserProfile

difficulty_levels = (
    (1, 'trivial'),
    (2, 'easy'),
    (3, 'moderate'),
    (4, 'difficult'),
    (5, 'extremely difficult')
)


class Challenge(models.Model):
    target = models.CharField(max_length=200, choices=settings.CHALLENGE_TYPES)
    type = models.CharField(max_length=200, choices=(('set', 'set'), ('numeric', 'numeric')))
    solarsystemobjects = models.ManyToManyField(SolarSystemObject, null=True, blank=True)
    astroobjects = models.ManyToManyField(AstroObject, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    rating = models.PositiveIntegerField(default=3, choices=difficulty_levels)
    number = models.PositiveIntegerField(default=1)
    multiplier = models.IntegerField(default=1)
    bonus = models.IntegerField(default=0)
    complete_bonus = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to="challenges", blank=True, null=True)

    class Meta:
        ordering = ['rating']

    def get_absolute_url(self):
        return urlresolvers.reverse("challenge-detail", args=(self.pk,))

    @property
    def all_objects(self):
        return set(self.solarsystemobjects.all()).union(set(self.astroobjects.all()))

    def __unicode__(self):
        return self.name


class CompletedChallenge(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    challenge = models.ForeignKey(Challenge)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'challenge')
        ordering = ['-date']

    def __unicode__(self):
        return "{0}-{1}-{2}".format(str(self.user_profile), str(self.challenge), str(self.date))
