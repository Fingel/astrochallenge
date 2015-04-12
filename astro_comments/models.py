from django_comments import Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
import logging
import datetime

logger = logging.getLogger(settings.DEFAULT_LOGGER)


class CustomComment(Comment):

    class Meta:
        ordering = ["-submit_date"]


@receiver(post_save, sender=CustomComment)
def send_comment_email(sender, instance, **kwargs):
    if instance.content_type == ContentType.objects.get(model='observation'):
        observation = instance.content_object
        if observation.user_profile.recieve_notification_emails and not instance.user == observation.user_profile.user:
                try:
                    from_user = instance.user
                    text = get_template('accounts/mail/comment.txt')
                    context = Context({'from_user': from_user.username, 'observation': observation, 'comment': instance.comment})
                    message = text.render(context)
                    subject = "{0} commented on your observation!".format(from_user.username)
                    to = (observation.user_profile.user.email,)
                    email = EmailMessage(subject=subject, body=message, to=to)
                    email.send()
                    logger.info('{0} EMAIL SENT: Subject: {1} Dest: {2}'.format(datetime.datetime.now(), subject, to))
                except Exception as exception:
                    logger.error('{0} EMAIL - EXCEPTION: Subject: {1} Dest: {2} {3}'.format(datetime.datetime.now(), subject, to, str(exception)))
