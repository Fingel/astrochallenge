from django.core.management.base import BaseCommand
from django.core.files import File
from astrochallenge.objects.models import CatalogObject
from decimal import *
import urllib


class Command(BaseCommand):
    args = '<catalog> <action>'
    help = "Import object images"

    def handle(self, *args, **options):
        catalog = args[0]
        for catalog_object in CatalogObject.objects.filter(catalog=catalog):
            astro_object = catalog_object.astro_object
            if args[1] == "download":
                if catalog == "M":
                    image = urllib.urlretrieve('http://messier.seds.org/Jpg/m{0}.jpg'.format(i))
                    astro_object.image.save('m{0}.jpg'.format(i), File(open(image[0])), save=False)
                    astro_object.save()
                    print "downloaded and set image for M{0}".format(catalog_object.designation)
                else:
                    pass
            else:
                if catalog == "M":
                    astro_object.image = 'astro_objects/m{0}.jpg'.format(catalog_object.designation)
                    astro_object.save()
                    print "set existing image for M{0}".format(catalog_object.designation)
