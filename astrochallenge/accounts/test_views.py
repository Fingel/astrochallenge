from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from test_helpers import AdminFactory, UserFactory


class AccountsViewTest(TransactionTestCase):
    def setUp(self):
        AdminFactory.build().save()
        UserFactory.build().save()

    def test_homepage(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Latest Observations", response.content)

        # Logged in
        login_result = self.client.login(username='stargazer', password='supersecret')
        self.assertTrue(login_result)
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Latest Observations", response.content)

    def test_login(self):
        response = self.client.get(reverse('auth_login'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('Login', response.content)

        data = {'username': 'notauser', 'password': 'supersecret'}

        response = self.client.post(reverse('auth_login'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn("Your username and password didn't match. Please try again.",
                      response.content)

        data['username'] = 'stargazer'
        response = self.client.post(reverse('auth_login'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        # Make sure the user is logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout(self):
        login_result = self.client.login(username='stargazer', password='supersecret')
        self.assertTrue(login_result)
        response = self.client.get(reverse('auth_logout'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("You have been sucessfully logged out", response.content)
        # Make sure the user is logged out
        self.assertIsNone(self.client.session.get('_auth_user_id'))

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

        # Make sure the user is logged in
        self.assertIsNotNone(self.client.session.get('_auth_user_id'))

        response = self.client.get('index')
        self.assertIn("Warning! You have not set your latitude/longitude!", response.content)
        self.assertIn('Logout', response.content)
