from django.forms.models import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.forms import HiddenInput, DateTimeField, ModelChoiceField
from django.utils import timezone
from django_markdown.widgets import MarkdownWidget

from models import Observation
from astrochallenge.accounts.models import Equipment


class ObservationForm(ModelForm):
    date = DateTimeField(initial=timezone.now)
    equipment = ModelChoiceField(queryset=Equipment.objects.none(), empty_label="None")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ObservationForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(user_profile=user.userprofile)

    class Meta:
        model = Observation
        fields = ('content_type', 'object_id', 'date', 'lat', 'lng', 'equipment', 'seeing', 'light_pollution', 'description')
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
            'description': MarkdownWidget(),
        }
        labels = {
            'description': 'Describe your observation. Markdown is used for formatting. Click the green "check" for a preview.'
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
