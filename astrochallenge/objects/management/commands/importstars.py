from django.core.management.base import BaseCommand
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation
from decimal import *
import csv
import ephem


class Command(BaseCommand):
    args = '<file>'
    help = "Import stars from the hyg database"

    def handle(self, *args, **options):
        astroobjects = {}
        with open(args[0], 'rb') as csvfile:
            mreader = csv.reader(csvfile)
            iteritems = iter(mreader)
            next(iteritems)  # Skip the first row
            next(iteritems)  # Skip the second row
            stars = 0
            for row in iteritems:
                if float(row[13]) < 3.8:
                    stars += 1
                    id = row[0]
                    hip = row[1]
                    hd = row[2]
                    bayer = row[27]
                    common_name = row[6]
                    ra = str(ephem.hours(row[7])).split(':')
                    dec = str(ephem.hours(row[8])).split(':')
                    distance = float(row[9]) * 3.262
                    magnitude = float(row[13])
                    constellation = Constellation.objects.get(abbreviation=row[29])
                    type = "Star"

                    ra_hours = float(ra[0])
                    ra_minutes = float(ra[1])
                    ra_seconds = float(ra[2])

                    dec_sign = '-' if dec[0][0] == '-' else '+'
                    dec_deg = float(dec[0].strip('-+'))
                    dec_min = float(dec[1])
                    dec_seconds = float(dec[2])

                    if not common_name:
                        if bayer:
                            common_name = '{0}{1}'.format(bayer, constellation.abbreviation)
                        else:
                            common_name = 'HIP{0}'.format(hip)
                    if hip or hd:  # dont save stars that have no designation in either of these catalogs
                        astro_object = {
                            'type': type,
                            'ra_hours': ra_hours,
                            'ra_minutes': ra_minutes,
                            'ra_seconds': ra_seconds,
                            'dec_sign': dec_sign,
                            'dec_deg': dec_deg,
                            'dec_min': dec_min,
                            'dec_seconds': dec_seconds,
                            'magnitude': magnitude,
                            'distance': distance,
                            'constellation': constellation,
                            'common_name': common_name,
                            'points': 1,
                            'hip': hip,
                            'hd': hd,
                        }
                        astroobjects[id] = astro_object

        #  Double star search
        with open(args[0], 'rb') as bcsvfile:
            breader = csv.reader(bcsvfile)
            doubleItems = iter(breader)
            next(doubleItems)
            next(doubleItems)
            for dRow in doubleItems:
                if dRow[30] != '1' and astroobjects.get(dRow[31], None):
                    if dRow[30] == '3':
                        astroobjects[dRow[31]]['type'] = "Triple Star"
                        astroobjects[dRow[31]]['points'] = 10
                    else:
                        astroobjects[dRow[31]]['type'] = "Double Star"
                        astroobjects[dRow[31]]['points'] = 10

        for key, astro_object in astroobjects.iteritems():
            hip = astro_object.get('hip')
            hd = astro_object.get('hd')
            del(astro_object['hip'])
            del(astro_object['hd'])

            astro_object = AstroObject(**astro_object)
            astro_object.save()
            print "sucessfully saved {0}".format(astro_object)
            if hip:
                catalog_object = CatalogObject(astro_object=astro_object, catalog="HIP", designation=str(hip))
                catalog_object.save()
                print "sucessfully saved {0}".format(catalog_object)
            if hd:
                catalog_object = CatalogObject(astro_object=astro_object, catalog="HD", designation=str(hd))
                catalog_object.save()
                print "sucessfully saved {0}".format(catalog_object)
