from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from datetime import datetime
import ephem

from astrochallenge.accounts.models import UserProfile


class Observation(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField()
    points_earned = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")

    def __unicode__(self):
        return "{0}-{1}".format(self.date, self.user_profile.user.username)

    @property
    def thing(self):
        thing = ""
        if self.content_type.model_class() == AstroObject:
            thing = "deep space object ({0})".format(self.content_object.type)
        elif self.content_type.model_class() == Constellation:
            thing = "constellation"
        return thing

    @property
    def name(self):
        name = ""
        if self.content_type.model_class() == AstroObject:
            name = str(self.content_object)
        elif self.content_type.model_class() == Constellation:
            name = self.content_object.latin_name
        return name

    @property
    def url(self):
        return urlresolvers.reverse("{0}-detail".format(self.content_type.model), args=(self.object_id,))


class Constellation(models.Model):
    abbreviation = models.CharField(max_length=3, unique=True)
    latin_name = models.CharField(max_length=200)
    latin_genitive = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="constellations", blank=True, null=True)

    def __unicode__(self):
        return self.latin_name


class AstroObject(models.Model):
    constellation = models.ForeignKey(Constellation, blank=True, null=True)
    type = models.CharField(max_length=200)
    ra_hours = models.IntegerField(blank=True, null=True)
    ra_minutes = models.FloatField(blank=True, null=True)
    dec_sign = models.CharField(max_length=1, choices=(('+', '+'), ('-', '-')), blank=True, default="")
    dec_deg = models.IntegerField(blank=True, null=True)
    dec_min = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    details = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    common_name = models.CharField(max_length=200, blank=True, default="")
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="astro_objects", blank=True, null=True)

    @property
    def ra_as_deg(self):
        return float(self.ra_hours * 15 + self.ra_minutes / 60)

    @property
    def dec_as_deg(self):
        degs = self.dec_deg + self.dec_min / 60
        multiplier = -1 if self.dec_sign == '-' else 1
        return degs * multiplier

    @property
    def fixed_body(self):
        object = ephem.FixedBody()
        object._ra = "{0}:{1}".format(self.ra_hours, self.ra_minutes)
        object._dec = "{0}{1}:{2}".format(self.dec_sign, self.dec_deg, self.dec_min)
        return object

    def __unicode__(self):
        return self.common_name if self.common_name else "{0}:{1}-{2}".format(self.constellation, self.ra_hours, self.dec_deg)

    def catalog_rep(self):
        ret_string = "/".join([str(co) for co in self.catalogobject_set.all()])
        ret_string += " ({0})".format(self.common_name) if self.common_name else ""
        return ret_string


class CatalogObject(models.Model):
    astro_object = models.ForeignKey(AstroObject)
    catalog = models.CharField(max_length=200, choices=settings.CATALOGS.items())
    designation = models.CharField(max_length=50)

    class Meta:
        unique_together = ('catalog', 'designation')

    def __unicode__(self):
        return "{0}{1}".format(self.catalog, self.designation)
