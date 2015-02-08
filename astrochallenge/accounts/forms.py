from django.contrib.auth.models import User
from django.forms.models import ModelForm

from models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.uf.fields.update(self.fields)
        self.fields = self.uf.fields

        self.uf.initial.update(self.initial)
        self.initial = self.uf.initial

    def save(self, *args, **kwargs):
        # save both forms
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = UserProfile
