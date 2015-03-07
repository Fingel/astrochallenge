from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.utils import timezone
from django.core import urlresolvers
import ephem
import pytz

from astrochallenge.accounts.models import UserProfile


class Observation(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField()
    points_earned = models.PositiveIntegerField(default=0)
    lat = models.FloatField("latitude", default=0.0)
    lng = models.FloatField("longitude", default=0.0)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ['-date']

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
        elif self.content_type.model_class() == SolarSystemObject:
            name = str(self.content_object)
        return name

    def get_absolute_url(self):
        return urlresolvers.reverse("{0}-detail".format(self.content_type.model), args=(self.object_id,))


class Constellation(models.Model):
    abbreviation = models.CharField(max_length=3, unique=True)
    latin_name = models.CharField(max_length=200)
    latin_genitive = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="constellations", blank=True, null=True)
    observations = GenericRelation(Observation)

    def __unicode__(self):
        return self.latin_name


class SolarSystemObject(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=settings.SOLAR_SYSTEM_OBJECT_TYPES)
    parent = models.ForeignKey('self', null=True, blank=True)
    index = models.IntegerField(default=999999)  # might want to add this to astroobject as well
    ephemeride = models.CharField(max_length=1000, default="")
    description = models.TextField(default="")
    mass = models.FloatField(null=True, blank=True)
    mass_unit = models.CharField(max_length=5, choices=(('s', 's'), ('e', 'e'), ('j', 'j'), ('kg', 'kg')), default="e")
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="ss_objects", blank=True, null=True)
    observations = GenericRelation(Observation)

    class Meta:
        ordering = ['index']

    @property
    def ephem_object(self):
        if self.ephemeride[:7] == 'pyephem':
            return getattr(ephem, self.ephemeride.split(':')[1])()
        else:
            try:
                return ephem.readdb(self.ephemeride)
            except:
                return None

    @property
    def general_info(self):
        p_object = self.ephem_object
        if p_object:
            p_object.compute()
            info = {
                "dec": str(p_object.dec),
                "ra": str(p_object.ra),
            }
            if self.type == 'P' or self.name == 'Moon':
                info.update({
                    "elongation": str(p_object.elong),
                    "earth_distance": str(p_object.earth_distance),
                    "sun_distance": str(p_object.sun_distance),
                    "phase": str(p_object.phase),
                    "magnitude": str(p_object.mag),
                })
            elif self.type == 'M' and self.name is not 'Moon':
                info.update({
                    "earth_visible": True if p_object.earth_visible > 0 else False,
                    "x": str(p_object.x),
                    "y": str(p_object.y),
                    "z": str(p_object.z),
                })
            return info
        else:
            return {}

    @property
    def ra(self):
        return self.general_info['ra']

    @property
    def dec(self):
        return self.general_info['dec']

    def observation_info(self, observer):
        p_object = self.ephem_object
        if p_object:
            p_object.compute(observer)
            up = True if ephem.degrees(p_object.alt) > 0 else False
            info = {
                'alt': str(p_object.alt),
                'az': str(p_object.az),
                'up': up,
            }
            if self.type == 'P' or self.name == 'Moon':
                info.update({
                    'rise': timezone.make_aware(observer.next_rising(p_object).datetime(), pytz.UTC) if observer.next_rising(p_object) else None,
                    'set': timezone.make_aware(observer.next_setting(p_object).datetime(), pytz.UTC) if observer.next_setting(p_object) else None,
                })

            return info
        else:
            return {}

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse("solarsystemobject-detail", args=(self.pk,))


class AstroObject(models.Model):
    constellation = models.ForeignKey(Constellation, blank=True, null=True)
    type = models.CharField(max_length=200)
    index = models.IntegerField(default=999999)
    ra_hours = models.IntegerField()
    ra_minutes = models.FloatField()
    dec_sign = models.CharField(max_length=1, choices=(('+', '+'), ('-', '-')), default="+")
    dec_deg = models.IntegerField()
    dec_min = models.FloatField()
    magnitude = models.FloatField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    details = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    common_name = models.CharField(max_length=200, blank=True, default="")
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="astro_objects", blank=True, null=True)
    observations = GenericRelation(Observation)

    class Meta:
        ordering = ['index']

    @property
    def ra(self):
        return "{0}:{1}:0".format(self.ra_hours, self.ra_minutes)

    @property
    def dec(self):
        return "{0}{1}:{2}:0".format(self.dec_sign, self.dec_deg, self.dec_min)

    @property
    def fixed_body(self):
        object = ephem.FixedBody()
        object._ra = "{0}:{1}".format(self.ra_hours, self.ra_minutes)
        object._dec = "{0}{1}:{2}".format(self.dec_sign, self.dec_deg, self.dec_min)
        return object

    def observation_info(self, observer):
        p_object = self.fixed_body
        p_object.compute(observer)
        up = True if ephem.degrees(p_object.alt) > 0 else False
        return {
            'alt': str(p_object.alt),
            'az': str(p_object.az),
            'up': up,
            'neverup': p_object.neverup,
            'rise': timezone.make_aware(observer.next_rising(p_object).datetime(), pytz.UTC) if observer.next_rising(p_object) else None,
            'set': timezone.make_aware(observer.next_setting(p_object).datetime(), pytz.UTC) if observer.next_setting(p_object) else None
        }

    def __unicode__(self):
        return self.common_name if self.common_name else "{0}:{1}-{2}".format(self.constellation, self.ra_hours, self.dec_deg)

    @property
    def catalog_rep(self):
        return ", ".join([str(co) for co in self.catalogobject_set.all()])

    def get_absolute_url(self):
        return urlresolvers.reverse("astroobject-detail", args=(self.pk,))


class CatalogObject(models.Model):
    astro_object = models.ForeignKey(AstroObject)
    catalog = models.CharField(max_length=200, choices=settings.CATALOGS.items())
    designation = models.CharField(max_length=50)

    class Meta:
        unique_together = ('catalog', 'designation')

    def __unicode__(self):
        return "{0}{1}".format(self.catalog, self.designation)
