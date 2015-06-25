from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from captcha.models import CaptchaStore
import base64
import datetime

from test_helpers import AdminFactory, UserFactory
from registration.models import RegistrationProfile
from astrochallenge.challenges.test_helpers import ChallengeFactory
from astrochallenge.objects.utils import moon_phase
from astrochallenge.objects.test_helpers import SolarSystemObjectObservationFactory, SolarSystemObjectFactory, SupernovaMagnitudeFactory


class AccountsViewTest(TransactionTestCase):
    def setUp(self):
        AdminFactory.create()
        self.user = UserFactory.create()
        self.challenge = ChallengeFactory.create(name="Test Challenge",
                                                 type='set')
        # need 1 comet for the homepage
        SolarSystemObjectFactory.create(type='C')

        # 1 supernova for the homepage
        SupernovaMagnitudeFactory.create()

    def test_homepage(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Latest Observations", response.content)
        self.assertIn(moon_phase(timezone.now())[1], response.content)

        # Logged in
        login_result = self.client.login(username=self.user.username, password='supersecret')
        self.assertTrue(login_result)
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Latest Observations", response.content)
        self.assertIn(self.challenge.name, response.content)

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


class AccountsProfileViewTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_profile_page(self):
        # Anonymous user
        response = self.client.get(reverse('profile', args=(self.user.username,)))
        self.assertEquals(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

        # logged in
        self.client.login(username=self.user.username, password='supersecret')
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

    def test_equipment(self):
        self.client.login(username=self.user.username, password='supersecret')
        response = self.client.post(reverse('add-equipment'),
                                    {'instrument': 'testscope'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('testscope', response.content)

        response = self.client.get(reverse('list-equipment'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('testscope', response.content)

        response = self.client.get(reverse('delete-equipment',
                                   args=(self.user.userprofile.equipment_set.first().id,)
                                   ), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)

    def test_edit_profile(self):
        self.client.login(username=self.user.username, password='supersecret')
        response = self.client.get(reverse('edit-profile'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('Edit profile', response.content)

        data = {
            'username': 'testuser',
            'location': 'anywhere USA',
            'timezone': 'America/Los_Angeles',
            'lat': 99999.0,
            'lng': 90.0,
            'elevation': 200,
            'profile_text': "my lat is WAY OFF!",
            'recieve_noification_emails': True
        }

        response = self.client.post(reverse('edit-profile'), data, follow=True)
        self.assertIn('Ensure this value is less than or equal to 90.0', response.content)

        data['lat'] = 45
        response = self.client.post(reverse('edit-profile'), data, follow=True)
        self.assertIn('Profile sucessfully updated', response.content)

    def test_observation_dates(self):
        observation = SolarSystemObjectObservationFactory.create(
            date=datetime.date.today() - datetime.timedelta(days=1),
            user_profile=self.user.userprofile
        )
        start_time = datetime.date.today() - datetime.timedelta(days=2),
        end_time = datetime.date.today()
        response = self.client.get(
            "{0}?start_time={1}&end_time={2}".format(
                reverse('profile', args=(self.user.username,)),
                start_time,
                end_time
            )
        )
        print response
        self.assertContains(response, observation.description)


class AccountsMiscViewTests(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.observation = SolarSystemObjectObservationFactory.create()

    def test_contact_form(self):
        captcha_count = CaptchaStore.objects.count()
        self.assertEqual(captcha_count, 0)

        response = self.client.get(reverse('contact'))
        self.assertEquals(response.status_code, 200)
        captcha_count = CaptchaStore.objects.count()
        self.assertEqual(captcha_count, 1)

        captcha = CaptchaStore.objects.first()
        data = {
            'email': 'contactemail@example.com',
            'feedback': 'I like ur site',
            'captcha_0': captcha.hashkey,
            'captcha_1': captcha.response
        }
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Thank you', response.content)

    def test_give_kudos(self):
        self.client.login(username=self.user.username, password='supersecret')
        response = self.client.get(
            reverse('give-kudos', args=(self.observation.id,))
        )
        self.assertContains(response, 'success')

        response = self.client.get(
            reverse('profile', args=(self.observation.user_profile.user.username,))
        )

        self.assertContains(response, 'Kudos: 1')


# Putting this here due to lack of other place to put it
class SitemapViewTest(TransactionTestCase):
    def test_sitemap(self):
        response = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertContains(response, 'urlset')
