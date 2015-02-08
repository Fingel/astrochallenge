import pytz
from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    timezone = TimeZoneField(default="UTC")
    location = models.CharField(max_length=200, blank=True)
    lat = models.DecimalField("latitude", max_digits=10, decimal_places=7, blank=True)
    lng = models.DecimalField("longitude", max_digits=10, decimal_places=7, blank=True)
    profile_text = models.TextField(blank=True)
