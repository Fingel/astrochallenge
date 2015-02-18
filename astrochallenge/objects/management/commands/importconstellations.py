from django.core.management.base import BaseCommand
from astrochallenge.objects.models import Constellation
from decimal import *
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
                abbreviation = row[0]
                latin_name = row[1]
                latin_genitive = row[2]
                english_name = row[3]

                constellation = Constellation(abbreviation=abbreviation, latin_name=latin_name, latin_genitive=latin_genitive, english_name=english_name)
                constellation.save()
                print "Saved {0}".format(constellation.latin_name)
