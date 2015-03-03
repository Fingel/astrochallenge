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
        labels = {
            'description': 'Describe your observation'
        }


class FinderChartForm(forms.Form):
    field_of_view = forms.FloatField(
        label="Field of view (degrees)",
        initial=15.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    limiting_magnitude_stars = forms.FloatField(
        label="Min. magnitude for stars",
        initial=10.0,
    )
    limiting_magnitude_deepsky = forms.FloatField(
        label="Min. magnitude for DSOs",
        initial=12.5
    )
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.IntegerField(widget=forms.HiddenInput)
