from django.forms.models import ModelForm
from django.forms import HiddenInput, DateTimeField
from django.utils.timezone import utc
from models import Observation
from datetime import datetime


class ObservationForm(ModelForm):
    date = DateTimeField(initial=datetime.now().replace(tzinfo=utc))

    class Meta:
        model = Observation
        fields = ('content_type', 'object_id', 'date', 'lat', 'lng', 'description')
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }
