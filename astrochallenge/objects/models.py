from django.db import models
from django.conf import settings


class AstroObject(models.Model):
    type = models.CharField(max_length=200)
    ra = models.DecimalField(max_digits=10, decimal_places=7)
    dec = models.DecimalField(max_digits=10, decimal_places=7)
    magnitude = models.DecimalField(max_digits=4, decimal_places=2)
    distance = models.IntegerField(default=0)
    size = models.DecimalField(max_digits=7, decimal_places=3)
    constellation = models.CharField(max_length=200, blank=True)
    detailed_type = models.CharField(max_length=200, blank=True)
    common_name = models.CharField(max_length=200, blank=True)
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="astro_objects", blank=True)

    def __unicode__(self):
        return self.common_name


class CatalogObject(models.Model):
    astro_object = models.ForeignKey(AstroObject)
    catalog = models.CharField(max_length=200, choices=settings.CATALOGS)
    designation = models.CharField(max_length=50)

    def __unicode__(self):
        return " {0} - {1}{2} ".format(self.astro_object.common_name, self.catalog, self.designation)