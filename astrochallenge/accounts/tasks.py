from __future__ import absolute_import
from celery import shared_task
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.dispatch import receiver
import logging

from astrochallenge.objects.models import Observation
from astro_comments.models import CustomComment

logger = logging.getLogger(settings.DEFAULT_LOGGER)


@shared_task
def kudos_email(from_user_id, observation_id):
    observation = Observation.objects.get(pk=observation_id)
    from_user = User.objects.get(pk=from_user_id)
    text = get_template('accounts/mail/kudos.txt')
    context = Context({'from_user': from_user.username, 'observation': observation})
    message = text.render(context)
    subject = "{0} gave you kudos on your observation!".format(from_user.username)
    to = (observation.user_profile.user.email,)
    email = EmailMessage(subject=subject, body=message, to=to)
    email.send()
    logger.info('EMAIL SENT: Subject: {0} Dest: {1}'.format(subject, to))


@shared_task
def comment_email(from_user_id, observation_id, comment_id):
    comment = CustomComment.objects.get(pk=comment_id)
    observation = Observation.objects.get(pk=observation_id)
    from_user = User.objects.get(pk=from_user_id)
    text = get_template('accounts/mail/comment.txt')
    context = Context({'from_user': from_user.username, 'observation': observation, 'comment': comment.comment})
    message = text.render(context)
    subject = "{0} commented on your observation!".format(from_user.username)
    to = (observation.user_profile.user.email,)
    email = EmailMessage(subject=subject, body=message, to=to)
    email.send()
    logger.info('EMAIL SENT: Subject: {0} Dest: {1}'.format(subject, to))


@receiver(post_save, sender=CustomComment)
def send_comment_email(sender, instance, **kwargs):
    if instance.content_type == ContentType.objects.get(model='observation'):
        observation = instance.content_object
        if observation.user_profile.recieve_notification_emails and not instance.user == observation.user_profile.user:
            comment_email.delay(instance.user.id, observation.id, instance.id)
