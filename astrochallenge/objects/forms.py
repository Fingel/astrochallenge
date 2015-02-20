from django.forms.models import ModelForm
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
