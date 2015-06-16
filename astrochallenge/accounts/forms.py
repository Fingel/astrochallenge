from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from captcha.fields import CaptchaField
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils import timezone


from models import UserProfile, Equipment


class ObservationLogForm(forms.Form):
    start_time = forms.DateField(required=False, widget=DateTimePicker(
            options={"format": "YYYY-MM-DD"}
        ))
    end_time = forms.DateField(required=False, widget=DateTimePicker(
            options={"format": "YYYY-MM-DD"}
        ))

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time > timezone.now().date():
            raise forms.ValidationError("You can't have observed anything in the future")
        return start_time


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    lat = forms.FloatField(
        label="Latitude (-90 to 90)",
        initial=0.0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
        )

    lng = forms.FloatField(
        label="Longitude (-180 to 180)",
        initial=0.0,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
        )

    class Meta:
        model = UserProfile
        fields = ('lat', 'lng', 'elevation', 'timezone', 'location', 'profile_text', 'recieve_notification_emails')


class EquipmentForm(ModelForm):
    instrument = forms.CharField(required=False)

    class Meta:
        model = Equipment
        fields = ('instrument',)


class ContactForm(forms.Form):
    email = forms.EmailField()
    feedback = forms.CharField(
            widget=forms.Textarea
        )
    captcha = CaptchaField()
