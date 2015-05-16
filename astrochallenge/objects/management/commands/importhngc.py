from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation
from datetime import date
from decimal import *


class Command(BaseCommand):
    args = '<file>'
    help = "Import historical ngc catalog items"

    classifications = {
        '*': 'Star',
        '**': 'Double Star',
        '***': 'Triple Star',
        'Ast': 'Asterism',
        'Gxy': 'Galaxy',
        'GxyCld': 'Nebulosity in External Galaxy',
        'Gc': 'Globular Cluster',
        'HIIRgn': 'HII Region',
        'Neb': 'Nebula',
        'NF': '?',
        'OC': 'Open Cluster',
        'PN': 'Planetary Nebula',
        'SNR': 'Supernova Remnant',
        'MWSC': 'Star Cloud',
    }

    def to_minutes(self, size):
        if size == '...' or size == '...\'':
            return 0
        if '"' in size:
            size = float(size.strip('"')) / 60
        else:
            size = float(size.strip('\''))
        return size

    def handle(self, *args, **options):
        with open(args[0], 'rb') as textfile:
            # skip first 9 lines
            for _ in xrange(9):
                next(textfile)
            for line in textfile:
                row = line.split('|')
                id = row[0]
                ra = row[5].split()
                ra_hours = int(ra[0].strip('h'))
                ra_minutes = int(ra[1].strip('m'))
                ra_seconds = float(ra[2].strip('s'))
                dec = row[6].split()
                dec_sign = dec[0][0]
                dec_deg = int(dec[0].strip('-').strip('+').strip('*'))
                dec_min = int(dec[1].strip('\''))
                dec_sec = float(dec[2].strip('"').strip('\'\''))
                constellation = Constellation.objects.get(abbreviation=row[7])
                details = row[8]
                discoverer = row[9]
                try:
                    discovery_date = date(int(row[10][:4]), 1, 1)
                except:
                    discovery_date = None
                classifcation = self.classifications.get(row[13], '?')
                size = row[15].replace('x', 'X').split('X')
                try:
                    arc_min = max(map(self.to_minutes, size))
                except:
                    arc_min = None
                magnitude = float(row[17] if row[17] != '...' else 9999)
                other_ngc = map(int, row[20].split('/') if row[20] != '...' and '?' not in row[20] else [])
                ic_desgs = map(int, row[21].split('/') if row[21] != '...' and '?' not in row[21] else [])

                astro_object = AstroObject(
                    type=classifcation,
                    ra_hours=ra_hours,
                    ra_minutes=ra_minutes,
                    ra_seconds=ra_seconds,
                    dec_sign=dec_sign,
                    dec_deg=dec_deg,
                    dec_min=dec_min,
                    dec_seconds=dec_sec,
                    constellation=constellation,
                    details=details,
                    discoverer=discoverer,
                    discovery_date=discovery_date,
                    size=arc_min,
                    magnitude=magnitude,
                    common_name="NGC{0}".format(id),
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
                    existing_astro_object = ca.astro_object
                    for attr, value in existing_astro_object.__dict__.iteritems():
                        if not value and getattr(astro_object, attr):
                            setattr(existing_astro_object, attr, getattr(astro_object, attr))
                            print "updated {0} with additional data for {1}".format(existing_astro_object, attr)

                    existing_astro_object.save()
                    for ngcid in other_ngc:
                        catalog_object = CatalogObject(astro_object=existing_astro_object,
                                                       catalog="NGC",
                                                       designation=str(ngcid))
                        try:
                            catalog_object.save()
                            print "created addtional catalog object {0}".format(catalog_object)
                        except:
                            pass

                    for icid in ic_desgs:
                        catalog_object = CatalogObject(astro_object=existing_astro_object,
                                                       catalog="IC",
                                                       designation=str(icid))
                        try:
                            catalog_object.save()
                            print "created addtional catalog object {0}".format(catalog_object)
                        except:
                            pass
                except ObjectDoesNotExist:
                    astro_object.save()
                    catalog_object = CatalogObject(astro_object=astro_object, catalog="NGC", designation="{0}".format(id))
                    catalog_object.save()
                    print "created {0} and added catalog object {1}".format(astro_object, catalog_object)
                    for ngcid in other_ngc:
                        catalog_object = CatalogObject(astro_object=astro_object,
                                                       catalog="NGC",
                                                       designation=str(ngcid))
                        try:
                            catalog_object.save()
                            print "created addtional catalog object {0}".format(catalog_object)
                        except:
                            pass
                    for icid in ic_desgs:
                        catalog_object = CatalogObject(astro_object=astro_object,
                                                       catalog="IC",
                                                       designation=str(icid))
                        try:
                            catalog_object.save()
                            print "created addtional catalog object {0}".format(catalog_object)
                        except:
                            pass
