from astro_comments.forms import SlimCommentForm
from astro_comments.models import CustomComment


def get_model():
    return CustomComment


def get_form():
    return SlimCommentForm
