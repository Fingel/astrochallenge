from django.core.management.base import BaseCommand
from django.core.files import File
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation
from decimal import *
import urllib
import csv


class Command(BaseCommand):
    args = '<file>'
    help = "Import Constellaion images"

    def handle(self, *args, **options):
        for constellation in Constellation.objects.all():
            if constellation.abbreviation is not "SB" and constellation.abbreviation is not "SH":
                print "getting image for {0}".format(constellation)
                image = urllib.urlretrieve('http://www.iau.org/static/public/constellations/gif/{0}.gif'.format(constellation.abbreviation.upper()))
                constellation.image.save('{0}.gif'.format(constellation.abbreviation), File(open(image[0])), save=False)
                constellation.save()
                print "saved image for {0}".format(constellation)
