from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.contenttypes.models import ContentType
from django_comments.forms import CommentSecurityForm
import datetime
import time
import json

from test_helpers import AstroObjectFactory, SolarSystemObjectFactory, AstroObjectObservationFactory, SolarSystemObjectObservationFactory, CatalogObjectFactory
from astrochallenge.accounts.test_helpers import UserFactory, EquipmentFactory
from astrochallenge.challenges.test_helpers import ChallengeFactory
from astro_comments.test_helpers import CustomCommentFactory


class ObjectsViewTests(TransactionTestCase):
    def setUp(self):
        self.astroobjects = AstroObjectFactory.create_batch(10)
        self.solarsystemobjects = SolarSystemObjectFactory.create_batch(3)
        self.ao = self.astroobjects[0]
        self.sso = self.solarsystemobjects[0]
        self.catalog_object = CatalogObjectFactory.create(astro_object=self.ao)
        self.user = UserFactory.create()
        self.equipment = EquipmentFactory(
            user_profile=self.user.userprofile,
            instrument='10in Dob'
        )
        self.single_challenge = ChallengeFactory.create(
            type='numeric',
            target='composite',
            number=1,
            name='first_challenge'
        )
        self.ao_challenge = ChallengeFactory.create(
            type='set',
            target='astro object',
            astroobjects=(self.ao,)
        )
        self.sso_challenge = ChallengeFactory.create(
            type='set',
            target='solar system object',
            solarsystemobjects=(self.solarsystemobjects)
        )

        self.ao_observation = AstroObjectObservationFactory.create(
            content_object=self.ao
        )
        self.sso_observation = SolarSystemObjectObservationFactory.create(
            content_object=self.sso
        )
        self.ao_comment = CustomCommentFactory.create(
            content_object=self.ao,
        )
        self.sso_comment = CustomCommentFactory.create(
            content_object=self.sso
        )

    def test_choose(self):
        response = self.client.get(reverse('choose-observation'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("What kind of object have you observed?", response.content)

    def test_astroobject_list(self):
        response = self.client.get(reverse('astroobject-list'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("All Deep Space Objects", response.content)

    def test_astroobject_json(self):
        # long-ass string warning
        response = self.client.get("/objects/dso/json?draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=false&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=designations&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=false&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false")
        # response = self.client.get('astroobject-list-json')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['recordsTotal'], 10)

        response = self.client.get(reverse(
            'astroobject-list-json',
            args=(self.ao.catalogobject_set.first().catalog,)))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'recordsTotal')

    def test_solarsystemobject_list_json(self):
        # long ass string warning
        response = self.client.get("/objects/solarsystem/json/?draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=false&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1434235570091")
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['recordsTotal'], 3)

    def test_solarsystemobject_list(self):
        response = self.client.get(reverse('solarsystemobject-list'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Solar System Objects", response.content)

    def test_astroobject_detail(self):
        response = self.client.get(reverse(
            'astroobject-detail',
            args=(self.ao.id,))
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn(self.ao.common_name, response.content)
        self.assertIn(self.ao.type, response.content)
        self.assertIn(self.ao_challenge.name, response.content)
        self.assertIn(self.ao_observation.description, response.content)
        self.assertIn('Please login to post comments', response.content)
        self.assertIn('Generate a finder chart', response.content)
        self.assertIn(self.ao_comment.comment, response.content)

    def test_astroobject_detail_by_catalog(self):
        response = self.client.get(reverse(
            'astroobject-detail',
            args=(self.ao.catalogobject_set.first().catalog,
                  self.ao.catalogobject_set.first().designation)
        ))
        self.assertEquals(response.status_code, 200)
        self.assertIn(self.ao.common_name, response.content)

    def test_solarsystemobject_detail(self):
        response = self.client.get(reverse(
            'solarsystemobject-detail',
            args=(self.sso.id,))
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.sso.name)
        self.assertContains(response, self.sso.type[1])
        self.assertContains(response, self.sso_challenge.name)
        self.assertContains(response, self.sso_observation.description)
        self.assertContains(response, 'Please login to post comments')
        self.assertContains(response, 'Generate a finder chart')
        self.assertContains(response, self.sso_comment.comment)

    def test_post_finderchart(self):
        content_type = ContentType.objects.get(model='astroobject')
        data = {
            'content_type': content_type.id,
            'object_id': self.ao.id,
            'date': datetime.datetime.now(),
            'field_of_view': 15.0,
            'limiting_magnitude_stars': 8.0,
            'limiting_magnitude_deepsky': 9.0,
        }
        response = self.client.post(
            reverse('post-finderchart'),
            data,
            follow=True
        )
        self.assertEquals(response.get('Content-Type'), 'application/pdf')
        self.assertTrue(response.get('Content-Length') > 0)

    def test_post_observation(self):
        self.client.login(username=self.user.username, password='supersecret')
        observation_count = len(self.user.userprofile.observation_set.all())
        points = self.user.userprofile.points
        completed_challenges = len(self.user.userprofile.completedchallenge_set.all())
        content_type = ContentType.objects.get(model='astroobject')
        data = {
            'content_type': content_type.id,
            'object_id': self.ao.id,
            'date': datetime.datetime.now(),
            'lat': 32.0,
            'lng': 122.0,
            'equipment': self.equipment.id,
            'seeing': 'A',
            'light_pollution': 'A',
            'featured': True,
            'image': None,
            'description': 'Test description for observation'

        }
        response = self.client.post(
            reverse('post-observation'),
            data,
            follow=True
        )
        self.assertContains(response, 'Observation recorded sucessfully')
        self.assertContains(response, self.single_challenge.name)
        self.assertContains(response, self.ao_challenge.name)
        self.assertEquals(
            len(self.user.userprofile.observation_set.all()),
            observation_count + 1
        )
        self.assertTrue(self.user.userprofile.points > points)
        self.assertTrue(
            len(self.user.userprofile.completedchallenge_set.all()) > completed_challenges
        )

        # Test invalid post
        data['equipment'] = 0
        response = self.client.post(
            reverse('post-observation'),
            data,
            follow=True
        )
        self.assertContains(response, "Error with observation submission")

    def test_delete_observation(self):
        self.client.login(username=self.user.username, password='supersecret')
        observation = AstroObjectObservationFactory.create(
            user_profile=self.user.userprofile
        )
        self.assertEquals(len(self.user.userprofile.observation_set.all()), 1)
        self.client.get(reverse('delete-observation',
            args=(observation.id,)
        ))
        self.assertEquals(len(self.user.userprofile.observation_set.all()), 0)

    def test_post_comment(self):
        self.client.login(username=self.user.username, password='supersecret')
        response = self.client.get(reverse(
            'astroobject-detail',
            args=(self.ao.id,))
        )
        post_time = int(time.time())
        data = {
            'content_type': 'objects.astroobject',
            'object_pk': self.ao.id,
            'timestamp': str(post_time),
        }
        form = CommentSecurityForm(self.ao)
        data['security_hash'] = form.initial_security_hash(post_time)
        data['comment'] = 'super secure comment'
        data['honeypot'] = ''
        response = self.client.post(
            reverse('comments-post-comment'),
            data,
            follow=True
        )
        self.assertContains(response, 'Thank you for your comment.')
