from django_comments.models import Comment
from django.conf import settings
import logging

logger = logging.getLogger(settings.DEFAULT_LOGGER)


class CustomComment(Comment):

    class Meta:
        ordering = ["-submit_date"]
        app_label = 'astro_comments'
