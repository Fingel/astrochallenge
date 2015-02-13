from django.db import models
from django.conf import settings


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
