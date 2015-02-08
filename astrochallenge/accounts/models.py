import pytz
from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    timezone = TimeZoneField(default="UTC")
    location = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    profile_text = models.TextField()
