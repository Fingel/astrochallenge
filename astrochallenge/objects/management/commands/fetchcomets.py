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
        self.logger.info("{0} - starting fetch comets.".format(datetime.datetime.now()))
        response = urllib2.urlopen('http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt')
        ss_objects = []
        sun = SolarSystemObject.objects.get(name='Sun')
        # search from botom up so we don't have to parse the entire list
        for line in response.readlines():
            if line[0] == '#':
                pass
            else:
                data = line.split(',')
                if SolarSystemObject.objects.filter(name=data[0]).exists():
                    self.logger.info("{0} - Skipped comet {1}".format(
                        datetime.datetime.now(),
                        data[0])
                    )
                    pass
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
                    points = 100
                ss_object.points = points
                ss_objects.append(ss_object)
        for sso in ss_objects:
            # so we get the new comets in the order in which they are added to
            # the remote list
            sso.date_added = timezone.now()
            # sso.save()
            self.logger.info("{0} - Added comet: {1} ({2} points) - {3}".format(
                datetime.datetime.now(), sso.name, sso.points, sso.date_added,
            ))
        self.logger.info("{0} - retrieved {1} comets.".format(
            datetime.datetime.now(), len(ss_objects))
        )
