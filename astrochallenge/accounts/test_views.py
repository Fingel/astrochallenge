from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from registration.models import RegistrationProfile


class AccountsViewTest(TransactionTestCase):
    def setUp(self):
        # Create an admin user
        User.objects.create(username='admin', password='password')

    def test_signup(self):
        response = self.client.get(reverse('registration_register'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Welcome to AstroChallenge!")

        data = {
            'username': 'admin',
            'password1': 'galaxy',
            'password2': 'galaxy',
            'email': 'test@example.com',
        }

        response = self.client.post(reverse('registration_register'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")

        data['username'] = 'galaxyfan'
        response = self.client.post(reverse('registration_register'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Please check your email to complete the registration process.")

        user = User.objects.get(username=data['username'])
        self.assertFalse(user.is_active)

        registration_profile = RegistrationProfile.objects.get(user=user)
        response = self.client.get(reverse('registration_activate',
                                           args=(registration_profile.activation_key,)),
                                   follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn("Yesss! Your account is activated.", response.content)

        response = self.client.get('index')
        self.assertIn("Warning! You have not set your latitude/longitude!", response.content)
        self.assertIn('Logout', response.content)
