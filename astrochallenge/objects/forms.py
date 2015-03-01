from django.forms.models import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.forms import HiddenInput, DateTimeField
from models import Observation
from django.utils import timezone


class ObservationForm(ModelForm):
    date = DateTimeField(initial=timezone.now)

    class Meta:
        model = Observation
        fields = ('content_type', 'object_id', 'date', 'lat', 'lng', 'description')
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }


class FinderChartForm(forms.Form):
    field_of_view = forms.FloatField(
        label="Field of view (degrees)",
        initial=7.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(50.0)]
    )
    limiting_magnitude_stars = forms.FloatField(
        label="Minimum magnitude for stars",
        initial=9.0,
    )
    limiting_magnitude_deepsky = forms.FloatField(
        label="Minimum magnite for deep sky objects",
        initial=12.5
    )
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.IntegerField(widget=forms.HiddenInput)
