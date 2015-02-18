from django.forms.models import ModelForm
from django import forms
from models import Observation
from datetime import datetime


class ObservationForm(ModelForm):
    date = forms.DateTimeField(initial=datetime.now)

    class Meta:
        model = Observation
        fields = ('date', 'lat', 'lng', 'description')
