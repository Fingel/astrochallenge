from django_comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings
import datetime

from astro_comments.models import CustomComment


class SlimCommentForm(CommentForm):

    def get_comment_model(self):
        return CustomComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and remove extra fields
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_unicode(self.target_object._get_pk_val()),
            comment=self.cleaned_data["comment"],
            submit_date=datetime.datetime.now(),
            site_id=settings.SITE_ID,
            is_public=True,
            is_removed=False,
        )


SlimCommentForm.base_fields.pop('url')
SlimCommentForm.base_fields.pop('email')
SlimCommentForm.base_fields.pop('name')
