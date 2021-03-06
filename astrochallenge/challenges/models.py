from django.db import models
from django.conf import settings
from django.core import urlresolvers
from django.utils import timezone
from operator import attrgetter

from astrochallenge.objects.models import AstroObject, SolarSystemObject, Supernova
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
    solarsystemobjects = models.ManyToManyField(SolarSystemObject, blank=True)
    astroobjects = models.ManyToManyField(AstroObject, blank=True)
    supernovae = models.ManyToManyField(Supernova, blank=True)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    rating = models.PositiveIntegerField(default=3, choices=difficulty_levels)
    number = models.PositiveIntegerField(default=1)
    multiplier = models.IntegerField(default=1)
    bonus = models.IntegerField(default=0)
    complete_bonus = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    index = models.PositiveIntegerField(default=9999)
    image = models.ImageField(upload_to="challenges", blank=True, null=True)

    class Meta:
        ordering = ['index', 'rating']

    def get_absolute_url(self):
        return urlresolvers.reverse("challenge-detail", args=(self.pk,))

    @staticmethod
    def current_challenges():
        return Challenge.objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now())

    @property
    def current(self):
        return self.start_time < timezone.now() and self.end_time > timezone.now()

    @property
    def all_objects(self):
        all_objects = list(self.solarsystemobjects.all())
        all_objects += list(self.astroobjects.all())
        all_objects += list(self.supernovae.all())
        return sorted(all_objects, key=attrgetter('pk'))

    @property
    def object_count(self):
        if self.type == "set":
            return self.solarsystemobjects.count() + self.astroobjects.count() + self.supernovae.count()
        else:
            return self.number

    def objects_observed(self, user):
        if self.type == "set":
            return len(set(self.all_objects).intersection(set([observation.content_object for observation in user.userprofile.observation_set.all()])))
        else:
            return min(self.number, user.userprofile.observation_set.count())

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
