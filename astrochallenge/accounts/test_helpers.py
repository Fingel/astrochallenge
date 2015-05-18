import factory
from django.contrib.auth.models import User


class AdminFactory(factory.Factory):
    class Meta:
        model = User

    username = 'admin'
    first_name = 'Admin'
    last_name = 'User'
    password = factory.PostGenerationMethodCall('set_password', 'supersecret')

    is_superuser = True


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'stargazer{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'supersecret')
    first_name = 'Edwin'
    last_name = 'Hubble'
    is_active = True
    email = factory.Sequence(lambda n: 'gazer{0}@example.com'.format(n))
