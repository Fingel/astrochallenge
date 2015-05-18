from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from registration.models import RegistrationProfile
from test_helpers import AdminFactory, UserFactory
import base64


class AccountsViewTest(TransactionTestCase):
    def setUp(self):
        AdminFactory.build().save()
        self.user = UserFactory.build()
        self.user.save()

    def test_homepage(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Latest Observations", response.content)

        # Logged in
        login_result = self.client.login(username=self.user.username, password='supersecret')
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

        data['username'] = self.user.username
        response = self.client.post(reverse('auth_login'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        # Make sure the user is logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout(self):
        login_result = self.client.login(username=self.user.username, password='supersecret')
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

    def test_reset_password(self):
        response = self.client.get(reverse('auth_password_reset'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('Reset your password', response.content)

        response = self.client.post(reverse('auth_password_reset'),
                                    {'email': self.user.email}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('email with a link to reset your password', response.content)

        pt = PasswordResetTokenGenerator()
        token = pt.make_token(self.user)
        uid = base64.b64encode(str(self.user.id)).strip('=')
        response = self.client.get(reverse('auth_password_reset_confirm',
                                           args=(uid, token)),
                                   follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Enter your new password below', response.content)

        data = {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }
        response = self.client.post(reverse('auth_password_reset_confirm', args=(uid, token)),
                                    data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Your password has been reset!', response.content)
        result = self.client.login(username=self.user.username, password='newpassword')
        self.assertTrue(result)

        #reset password
        self.user.set_password('supersecret')

    def test_change_password(self):
        self.assertTrue(self.client.login(username=self.user.username, password='supersecret'))
        response = self.client.get(reverse('auth_password_change'))
        self.assertEquals(response.status_code, 200)

        data = {
            'old_password': 'supersecret',
            'new_password1': 'newpassword',
            'new_password2': 'newpasswordnotright'
        }

        response = self.client.post(reverse('auth_password_change'), data, follow=True)
        self.assertIn('The two password fields didn&#39;t match', response.content)

        data['new_password2'] = 'newpassword'
        response = self.client.post(reverse('auth_password_change'), data, follow=True)
        self.assertIn('Password successfully changed', response.content)

        u = User.objects.get(pk=self.user.id)
        self.assertTrue(u.check_password('newpassword'))
