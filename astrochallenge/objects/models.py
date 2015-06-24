from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.core import urlresolvers
from scipy import optimize
import ephem
import logging
import pytz
import datetime

from astrochallenge.accounts.models import UserProfile, Equipment
from astrochallenge.objects.utils import calculate_points, FixedElement

logger = logging.getLogger(settings.DEFAULT_LOGGER)


class Observation(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField()
    points_earned = models.PositiveIntegerField(default=0)
    lat = models.FloatField("latitude", default=0.0)
    lng = models.FloatField("longitude", default=0.0)
    equipment = models.ForeignKey(Equipment, null=True, blank=True)
    seeing = models.CharField(max_length=2, choices=settings.QUALITATIVE_RATINGS, default='A')
    light_pollution = models.CharField(max_length=2, choices=settings.QUALITATIVE_RATINGS, default='A')
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="observations", blank=True, null=True, help_text="Maximum file size: 50mb.")
    featured = models.BooleanField(default=False, help_text="Feature this observation on your profile.")

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return "{0} {1}: {2}".format(self.user_profile.user.username, self.date.strftime('%m/%d/%y'), str(self.content_object))

    @property
    def name(self):
        if self.content_type.model_class() == Constellation:
            return self.content_object.latin_name
        else:
            return str(self.content_object)

    def get_absolute_url(self):
        return urlresolvers.reverse("observation-detail", args=(self.pk,))


class Constellation(models.Model):
    abbreviation = models.CharField(max_length=3, unique=True)
    latin_name = models.CharField(max_length=200)
    latin_genitive = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="constellations", blank=True, null=True)
    observations = GenericRelation(Observation)

    def __unicode__(self):
        return self.latin_name

    def get_absolute_url(self):
        return urlresolvers.reverse("constellation-detail", args=(self.pk,))


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
    image_attribution = models.CharField(max_length=1000, default="", blank=True)
    observations = GenericRelation(Observation)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['index']

    @property
    def bonus_points(self):
        return calculate_points(self) - self.points

    @property
    def constellation(self):
        p_object = self.ephem_object
        if p_object:
            p_object.compute()
            try:
                abbrv = ephem.constellation(p_object)[0]
                return Constellation.objects.get(abbreviation=abbrv)
            except:
                return None
        else:
            return None

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
            if self.type != 'M':
                info.update({
                    "elongation": str(p_object.elong),
                    "earth_distance": str(p_object.earth_distance),
                    "sun_distance": str(p_object.sun_distance),
                    "magnitude": str(p_object.mag),
                })

            if self.type == 'P' or self.name == 'Moon':
                info.update({
                    "phase": str(p_object.phase),
                })
            elif self.type == 'C':
                info.update({
                    "peak_magnitude": self.peak_magnitude,
                    "closest_approach": self.min_earth_distance
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

    def ra_dec_on_date(self, date):
        p_object = self.ephem_object
        if p_object:
            p_object.compute(date)
            return (str(p_object.dec), str(p_object.dec))
        else:
            return (None, None)

    @property
    def peak_magnitude(self):
        return self.compute_min_property('mag')

    @property
    def min_earth_distance(self):
        return self.compute_min_property('earth_distance')

    def compute_min_property(self, prop):
        ephemeride = self.ephem_object

        def compute_min(time):
            ephemeride.compute(time)
            return getattr(ephemeride, prop)

        if ephemeride:
            now = ephem.now()
            # 100 year from now bounds
            bounds = [ephem.Date(now - ephem.hour * 24 * 365 * 100),
                      ephem.Date(now + ephem.hour * 24 * 365 * 100)]
            result = optimize.minimize_scalar(
                compute_min,
                method='Bounded',
                bounds=bounds
            )
            if result['message'] == 'Solution found.':
                ephemeride.compute(result['x'])
                data = {
                    'ephemeride': ephemeride,
                    'date': ephem.Date(result['x']).datetime()
                }
                data[prop] = getattr(ephemeride, prop)
                return data
            else:
                return None
        else:
            return None

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
            try:
                info.update({
                    'neverup': p_object.neverup
                })
            except:
                pass
            try:
                next_rising = observer.next_rising(p_object)
                next_setting = observer.next_setting(p_object)
                info.update({
                    'rise': timezone.make_aware(next_rising.datetime(), pytz.UTC) if next_rising else None,
                    'set': timezone.make_aware(next_setting.datetime(), pytz.UTC) if next_setting else None,
                })
            except ephem.AlwaysUpError:
                info.update({
                    'alwaysup': True
                })
            except:
                pass

            return info

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse("solarsystemobject-detail", args=(self.pk,))


class AstroObject(models.Model, FixedElement):
    constellation = models.ForeignKey(Constellation, blank=True, null=True)
    type = models.CharField(max_length=200)
    index = models.IntegerField(default=999999)
    ra_hours = models.IntegerField()
    ra_minutes = models.FloatField()
    ra_seconds = models.FloatField(default=0.0, blank=True)
    dec_sign = models.CharField(max_length=1, choices=(('+', '+'), ('-', '-')), default="+")
    dec_deg = models.IntegerField()
    dec_min = models.FloatField()
    dec_seconds = models.FloatField(default=0.0, blank=True)
    magnitude = models.FloatField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    details = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    common_name = models.CharField(max_length=200, blank=True, default="")
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="astro_objects", blank=True, null=True)
    image_attribution = models.CharField(max_length=1000, default="", blank=True)
    discoverer = models.CharField(max_length=200, default="", blank=True)
    discovery_date = models.DateField(blank=True, null=True)
    observations = GenericRelation(Observation)

    class Meta:
        ordering = ['index']

    @property
    def bonus_points(self):
        return calculate_points(self) - self.points

    @property
    def ra(self):
        return "{0}:{1}:{2}".format(self.ra_hours, self.ra_minutes, self.ra_seconds)

    @property
    def dec(self):
        return "{0}{1}:{2}:{3}".format(self.dec_sign, self.dec_deg, self.dec_min, self.dec_seconds)

    def __unicode__(self):
        return self.common_name if self.common_name else "{0}:{1}-{2}".format(self.constellation, self.ra_hours, self.dec_deg)

    @property
    def catalog_rep(self):
        return ", ".join([str(co) for co in self.catalogobject_set.all()])

    def get_absolute_url(self):
        return urlresolvers.reverse("astroobject-detail", args=(self.pk,))

    def get_magnitude_display(self):
        if self.magnitude > 100:
            return ""
        else:
            return str(self.magnitude)


class CatalogObject(models.Model):
    astro_object = models.ForeignKey(AstroObject)
    catalog = models.CharField(max_length=200, choices=settings.CATALOGS.items())
    designation = models.CharField(max_length=50)

    class Meta:
        unique_together = ('catalog', 'designation')

    def __unicode__(self):
        return "{0}{1}".format(self.catalog, self.designation)


class Supernova(models.Model, FixedElement):
    name = models.CharField(max_length=255, unique=True)
    astro_object = models.ForeignKey(AstroObject, null=True, blank=True, default=None)
    ra_hours = models.IntegerField()
    ra_minutes = models.FloatField()
    ra_seconds = models.FloatField(default=0.0, blank=True)
    dec_sign = models.CharField(max_length=1, choices=(('+', '+'), ('-', '-')), default="+")
    dec_deg = models.IntegerField()
    dec_min = models.FloatField()
    dec_seconds = models.FloatField(default=0.0, blank=True)
    discovery_date = models.DateTimeField()
    sntype = models.CharField(max_length=255)
    z = models.FloatField(blank=True, null=True)
    points = models.IntegerField(default=10)
    date_added = models.DateTimeField(default=timezone.now)

    @staticmethod
    def brightest_supernova():
        try:
            return SupernovaMagnitude.objects.filter(
                time__gt=timezone.now() - datetime.timedelta(days=30)
            ).order_by('magnitude')[:1][0].supernova
        except:
            logger.error("no SN readings in the last month!")
            return Supernova.objects.last()

    def latest_magnitude(self):
        return self.supernovamagnitude_set.order_by('-time').first()

    @property
    def constellation(self):
        p_object = self.fixed_body
        if p_object:
            p_object.compute()
            try:
                abbrv = ephem.constellation(p_object)[0]
                return Constellation.objects.get(abbreviation=abbrv)
            except:
                return None
        else:
            return None


class SupernovaMagnitude(models.Model):
    supernova = models.ForeignKey(Supernova)
    magnitude = models.FloatField()
    time = models.DateTimeField()
