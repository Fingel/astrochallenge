from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator


from models import UserProfile, Equipment


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
        fields = '__all__'


class EquipmentForm(ModelForm):
    instrument = forms.CharField(required=False)

    class Meta:
        model = Equipment
        fields = ('instrument',)
