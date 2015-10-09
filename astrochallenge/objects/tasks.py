from __future__ import absolute_import
from celery import shared_task
from astrochallenge.objects.models import SolarSystemObject, CatalogObject, Supernova, SupernovaMagnitude
from django.conf import settings
from django.utils import timezone
import logging
from decimal import *
import urllib2
import datetime
import pytz
import re

logger = logging.getLogger(settings.DEFAULT_LOGGER)


@shared_task
def update_sso_magnitude():
    logger.info('starting update sso magnitude')
    for sso in SolarSystemObject.objects.all():
        try:
            sso.magnitude = float(sso.general_info.get('magnitude'))
        except:
            sso.magnitude = None
        sso.save()
    logger.info('finished update sso magnitude')


@shared_task
def fetch_supernovae():
    logger.info("starting fetch supernovae")
    response = urllib2.urlopen("http://www.rochesterastronomy.org/snimages/snmag.html")
    fulltext = response.read()
    text = fulltext[fulltext.index('<pre>'):fulltext.index('</pre>')]
    lines = text.splitlines()[3:]
    cnt = 0
    for line in lines:
        record = line.split()

        # Discovery date
        discovery_date = datetime.datetime.strptime(record[2].split('.')[0], "%Y/%m/%d")
        discovery_date = discovery_date.replace(tzinfo=pytz.UTC)

        # Get magnitude and time
        last_mag = float(record[3].strip('*'))
        last_mag_date = datetime.datetime.strptime(
            "{0}/{1}".format(str(discovery_date.year), record[4]),
            "%Y/%m/%d")
        last_mag_date = last_mag_date.replace(tzinfo=pytz.UTC)
        max_mag = float(record[5])
        max_mag_date = datetime.datetime.strptime(
            "{0}/{1}".format(str(discovery_date.year), record[6]),
            "%Y/%m/%d")
        max_mag_date = max_mag_date.replace(tzinfo=pytz.UTC)

        if last_mag_date < timezone.now() - datetime.timedelta(days=365):
            pass

        else:
            # Get the easy stuff
            sntype = record[7]
            try:
                z = float(record[8])
            except:
                z = None

            # Parse RA and DEC
            ra = record[0].split(':')
            dec = record[1].split(':')
            ra_hours = float(ra[0])
            ra_minutes = float(ra[1])
            ra_seconds = float(ra[2])
            dec_sign = dec[0][:1]
            dec_deg = float(dec[0][1:])
            dec_min = float(dec[1])
            dec_seconds = float(dec[2])

            # Get catalog designation of astroobject, if any
            if len(record) == 13:  # the catalog name is probably split
                catalog = record[9]
                designation = record[10]
            else:
                des = re.split('(\d+)', record[9])
                if len(des) == 2:
                    catalog = des[0]
                    designation = des[1]
                else:
                    catalog, designation = 'unk', 'unk'
            if CatalogObject.objects.filter(catalog=catalog, designation=designation).exists():
                astroobject = CatalogObject.objects.get(catalog=catalog, designation=designation).astro_object
            else:
                astroobject = None

            # Get the damn name
            nametext = ' '.join(record[record.index('<a'):])
            name = nametext[nametext.index('>'):nametext.index('</a>')][1:]

            if Supernova.objects.filter(name=name).exists():
                sn = Supernova.objects.get(name=name)
            else:
                sn = Supernova.objects.create(
                        name=name,
                        astro_object=astroobject,
                        ra_hours=ra_hours,
                        ra_minutes=ra_minutes,
                        ra_seconds=ra_seconds,
                        dec_sign=dec_sign,
                        dec_deg=dec_deg,
                        dec_min=dec_min,
                        dec_seconds=dec_seconds,
                        discovery_date=discovery_date,
                        sntype=sntype,
                        z=z
                    )
                cnt = cnt + 1
            if not sn.supernovamagnitude_set.filter(magnitude=last_mag, time=last_mag_date).exists():
                SupernovaMagnitude.objects.create(supernova=sn, magnitude=last_mag, time=last_mag_date)
            if not sn.supernovamagnitude_set.filter(magnitude=max_mag, time=max_mag_date).exists():
                SupernovaMagnitude.objects.create(supernova=sn, magnitude=max_mag, time=max_mag_date)
    logger.info("retrieved {0} new supernovae".format(cnt))


@shared_task
def fetch_comets():
    logger.info("starting fetch comets.")
    response = urllib2.urlopen('http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt')
    ss_objects = []
    sun = SolarSystemObject.objects.get(name='Sun')
    for line in response.readlines():
        if line[0] == '#':
            pass
        else:
            data = line.split(',')
            if SolarSystemObject.objects.filter(name=data[0]).exists():
                pass
            else:
                ss_object = SolarSystemObject(
                    index=999999,
                    name=data[0],
                    type='C',
                    ephemeride=line,
                    parent=sun,
                )
                magnitude = ss_object.peak_magnitude['mag']
                points = 1
                if magnitude < 18:
                    points = 10
                if magnitude < 16:
                    points = 20
                if magnitude < 12:
                    points = 30
                if magnitude < 10:
                    points = 50
                if magnitude < 7:
                    points = 75
                ss_object.points = points
                ss_objects.append(ss_object)
    for sso in ss_objects:
        sso.date_added = timezone.now()
        sso.save()
        logger.info("Added comet: {0} ({1} points) - {2}".format(
            sso.name, sso.points, sso.date_added,
        ))
    logger.info("retrieved {0} comets.".format(len(ss_objects)))
