from django.contrib.auth.models import User
from django.forms.models import ModelForm

from models import UserProfile, Equipment


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ('instrument',)
