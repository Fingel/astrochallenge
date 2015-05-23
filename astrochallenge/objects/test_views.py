from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
import json

from test_helpers import AstroObjectFactory, SolarSystemObjectFactory, AstroObjectObservationFactory, SolarSystemObjectObservationFactory
from astrochallenge.accounts.test_helpers import UserFactory
from astrochallenge.challenges.test_helpers import ChallengeFactory
from astro_comments.test_helpers import CustomCommentFactory


class ObjectsViewTests(TransactionTestCase):
    def setUp(self):
        self.astroobjects = AstroObjectFactory.create_batch(10)
        self.solarsystemobjects = SolarSystemObjectFactory.create_batch(3)
        self.user = UserFactory.create()
        self.ao_challenge = ChallengeFactory.create(
            type='set',
            astroobjects=(self.astroobjects[:3])
        )
        self.sso_challenge = ChallengeFactory.create(
            type='set',
            solarsystemobjects=(self.solarsystemobjects)
        )
        self.ao = self.astroobjects[0]
        self.sso = self.solarsystemobjects[0]

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
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['recordsTotal'], 10)

    def test_solarsystemobject_list(self):
        response = self.client.get(reverse('solarsystemobject-list'))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Solar System Objects", response.content)
        self.assertIn(self.sso.name, response.content)

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
