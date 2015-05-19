from django.contrib.auth.models import User
from django.db.models import signals
from models import UserProfile
import factory
import random


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'admin'
    first_name = 'Admin'
    last_name = 'User'
    password = factory.PostGenerationMethodCall('set_password', 'supersecret')

    is_superuser = True


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    timezone = "UTC"
    location = "Santa Cruz"
    lat = factory.LazyAttribute(lambda x: random.randint(-45, 45))
    lng = factory.LazyAttribute(lambda x: random.randint(-180, 180))
    elevation = factory.LazyAttribute(lambda x: random.randint(0, 4000))
    profile_text = "Test user please ignore"
    recieve_notification_emails = True
    user = factory.SubFactory('app.factories.UserFactory', userprofile=None)


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'stargazer{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'supersecret')
    first_name = 'Edwin'
    last_name = 'Hubble'
    is_active = True
    email = factory.Sequence(lambda n: 'gazer{0}@example.com'.format(n))
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')
