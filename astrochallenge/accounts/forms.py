from django.contrib.auth.models import User
from django.forms.models import ModelForm

from models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile

