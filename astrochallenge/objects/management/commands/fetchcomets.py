from django.core.management.base import BaseCommand
from astrochallenge.objects.models import SolarSystemObject
from django.conf import settings
from django.utils import timezone
import datetime
import logging
from decimal import *
import urllib2


class Command(BaseCommand):
    args = 'none'
    help = "Download latest comets from http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt"
    logger = logging.getLogger(settings.DEFAULT_LOGGER)

    def handle(self, *args, **options):
        response = urllib2.urlopen('http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt')
        ss_objects = []
        sun = SolarSystemObject.objects.get(name='Sun')
        # search from botom up so we don't have to parse the entire list
        for line in reversed(response.readlines()):
            if line[0] == '#':
                pass
            else:
                data = line.split(',')
                if SolarSystemObject.objects.filter(name=data[0]).exists():
                    break
                ss_object = SolarSystemObject(
                    index=999999,
                    name=data[0],
                    type='C',
                    ephemeride=line,
                    points=1,
                    parent=sun,
                )
                ss_objects.append(ss_object)
        for sso in reversed(ss_objects):
            # so we get the new comets in the order in which they are added to
            # the remote list
            sso.date_added = timezone.now()
            sso.save()
            self.logger.info("{0} Added comet: {1} - {2}".format(
                datetime.datetime.now(), sso.name, sso.date_added
            ))
