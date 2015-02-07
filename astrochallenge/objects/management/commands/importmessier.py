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
            i = 1
            for row in iteritems:
                astro_object = AstroObject(type=row[1], ra=Decimal(row[2]), dec=Decimal(row[3]), magnitude=Decimal(row[4]), distance=0, size=Decimal(row[5]), constellation=row[7],
                    detailed_type=row[8])
                if len(row) > 9:
                    astro_object.common_name = row[9]
                else:
                    astro_object.common_name = row[0]
                if not astro_object.common_name or astro_object.common_name == '':
                    astro_object.common_name = row[0]
                points = 1
                if float(row[4]) < 10:
                    points = 10
                if float(row[4]) < 8:
                    points = 20
                if float(row[4]) < 6:
                    points = 30
                if float(row[4]) < 4:
                    points = 50
                if float(row[4]) < 2:
                    points = 100
                astro_object.points = points
                print "getting image"
                image = urllib.urlretrieve('http://messier.seds.org/Jpg/m{0}.jpg'.format(i))
                astro_object.image.save('m{0}.jpg'.format(i), File(open(image[0])), save=False)
                astro_object.save()
                print "sucessfully saved {0}".format(astro_object.common_name)
                catalog_object = CatalogObject(astro_object=astro_object, catalog="M", designation="{0}".format(i))
                catalog_object.save()
                print "sucessfully saved {0}".format(catalog_object)
                i = i + 1



