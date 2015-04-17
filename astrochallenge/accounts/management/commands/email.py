import sys
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
import logging
import datetime


class Command(BaseCommand):
    logger = logging.getLogger(settings.DEFAULT_LOGGER)

    def handle(self, *args, **options):
        to = [args[0], ]
        subject = raw_input("Subject--> ")
        print("Body:")
        body = sys.stdin.read()
        email = EmailMessage(subject=subject, body=body, to=to, from_email="info@astrochallenge.com")
        try:
            email.send()
            print ("\nEmail sent successfully")
            self.logger.info('{0} EMAIL SENT: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
        except Exception as exception:
            self.logger.error('{0} EMAIL - EXCEPTION: Subject: {1} Dest: {2} {3}'.format(datetime.datetime.now(), subject, to, str(exception)))
