from django.forms.models import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django import forms
from django.forms import HiddenInput, DateTimeField, ModelChoiceField
from django.utils import timezone
from django_markdown.widgets import MarkdownWidget
from bootstrap3_datetime.widgets import DateTimePicker

from models import Observation
from astrochallenge.accounts.models import Equipment


class ObservationLogForm(forms.Form):
    start_time = DateTimeField(widget=DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm:ss"}
        ))
    end_time = DateTimeField(widget=DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm:ss"}
        ))


class ObservationForm(ModelForm):
    date = DateTimeField(initial=timezone.now, widget=DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm:ss"}
        ))
    equipment = ModelChoiceField(queryset=Equipment.objects.none(), empty_label="Not specified", required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ObservationForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(user_profile=user.userprofile)

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now():
            raise forms.ValidationError("Unless you've learned to bend the laws of time and space, you can't observe in the future!")
        return date

    def clean_image(self):
        image = self.cleaned_data['image']
        if image and image.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Image is too large! Image must be less than 50mb in size.")
        return image

    class Meta:
        model = Observation
        fields = ('content_type', 'object_id', 'date', 'lat', 'lng', 'equipment', 'seeing', 'light_pollution', 'description', 'image', 'featured')
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
        label="F.O.V (deg)",
        initial=15.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    limiting_magnitude_stars = forms.FloatField(
        label="Min. mag for stars",
        initial=10.0,
    )
    limiting_magnitude_deepsky = forms.FloatField(
        label="Min. mag for DSOs",
        initial=12.5
    )
    date = forms.DateTimeField(
        initial=timezone.now,
        widget=DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm:ss"}
        )
    )
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.IntegerField(widget=forms.HiddenInput)
