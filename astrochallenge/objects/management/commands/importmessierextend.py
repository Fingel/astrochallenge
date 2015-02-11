from django.core.management.base import BaseCommand
from django.core.files import File
from astrochallenge.objects.models import AstroObject, CatalogObject
from decimal import *
import urllib
import csv


class Command(BaseCommand):
    args = '<file>'
    help = "Import messier catalog items"

    def handle(self, *args, **options):
        with open(args[0], 'rb') as csvfile:
            mreader = csv.reader(csvfile)
            iteritems = iter(mreader)
            next(iteritems)  # Skip the first row
            for row in iteritems:
                id = row[0]
                ngc = row[1]
                type = row[2]
                constellation = row[3]
                ra_hours = row[4]
                ra_minutes = float(row[5])
                dec_sign = row[6]
                dec_deg = row[7]
                dec_min = float(row[8])
                magnitude = float(row[9])
                size = float(row[10])
                distance = float(row[11])
                try:
                    common_name = row[12]
                except:
                    common_name = ""

                astro_object = AstroObject(
                    type=type,
                    ra_hours=ra_hours,
                    ra_minutes=ra_minutes,
                    dec_sign=dec_sign,
                    dec_deg=dec_deg,
                    dec_min=dec_min,
                    magnitude=magnitude,
                    size=size,
                    distance=distance,
                    constellation=constellation,
                    common_name=common_name,
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
                # print "getting image"
                # image = urllib.urlretrieve('http://messier.seds.org/Jpg/m{0}.jpg'.format(i))
                # astro_object.image.save('m{0}.jpg'.format(i), File(open(image[0])), save=False)
                astro_object.save()
                print "sucessfully saved {0}".format(astro_object.common_name)
                catalog_object = CatalogObject(astro_object=astro_object, catalog="M", designation="{0}".format(id))
                catalog_object.save()
                print "sucessfully saved {0}".format(catalog_object)
                catalog_object = CatalogObject(astro_object=astro_object, catalog="NGC", designation="{0}".format(ngc[3:]))
                catalog_object.save()
                print "sucessfully saved {0}".format(catalog_object)
