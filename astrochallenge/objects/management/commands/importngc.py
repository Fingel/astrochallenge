from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation
from decimal import *
import urllib
import csv


class Command(BaseCommand):
    args = '<file>'
    help = "Import ngc catalog items"

    def handle(self, *args, **options):
        with open(args[0], 'rb') as csvfile:
            mreader = csv.reader(csvfile)
            iteritems = iter(mreader)
            next(iteritems)  # Skip the first row
            for row in iteritems:
                id = row[0]
                try:
                    type = row[2]
                except:
                    type = "Unknown"
                constellation = Constellation.objects.get(abbreviation=row[3])
                try:
                    magnitude = float(row[4])
                except:
                    magnitude = 9999
                details = row[5]
                ra_hours = row[6]
                ra_minutes = float(row[7])
                dec_sign = row[8]
                dec_deg = row[9]
                dec_min = float(row[10])

                astro_object = AstroObject(
                    type=type,
                    ra_hours=ra_hours,
                    ra_minutes=ra_minutes,
                    dec_sign=dec_sign,
                    dec_deg=dec_deg,
                    dec_min=dec_min,
                    magnitude=magnitude,
                    details=details,
                    constellation=constellation,
                )
                points = 1
                if magnitude < 10:
                    points = 10
                if magnitude < 8:
                    points = 20
                if magnitude < 6:
                    points = 30
                if magnitude < 4:
                    points = 50
                if magnitude < 2:
                    points = 100
                astro_object.points = points
                try:
                    ca = CatalogObject.objects.get(catalog="NGC", designation=id)
                    astro_object = ca.astro_object
                    astro_object.details = details
                    astro_object.save()
                    print "updated {0} with details".format(astro_object)
                except ObjectDoesNotExist:
                    astro_object.save()
                    catalog_object = CatalogObject(astro_object=astro_object, catalog="NGC", designation="{0}".format(id))
                    catalog_object.save()
                    print "created {0} and added catalog object {1}".format(astro_object, catalog_object)
