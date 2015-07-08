from django.core.urlresolvers import reverse
from django.test import TransactionTestCase

from astrochallenge.objects.test_helpers import (AstroObjectFactory,
    AstroObjectObservationFactory)
from astrochallenge.accounts.test_helpers import UserFactory
from astrochallenge.challenges.test_helpers import ChallengeFactory


class ChallengeViewTests(TransactionTestCase):
    def setUp(self):
        self.astroobjects = AstroObjectFactory.create_batch(5)
        self.single_challenge = ChallengeFactory.create(
            type='numeric',
            target='composite',
            number=1,
            name='first_challenge'
        )
        self.ao_challenge = ChallengeFactory.create(
            type='set',
            target='astro object',
            astroobjects=(self.astroobjects)
        )
        self.user = UserFactory.create()
        self.ao_observation = AstroObjectObservationFactory.create(
            content_object=self.astroobjects[0]
        )

    def test_sigimage(self):
        response = self.client.get(
            "{0}?user={1}&challenges={2},{3}".format(
                reverse('sigimage'), self.user.id, self.single_challenge.id, self.ao_challenge.id)
        )
        self.assertEquals(response.status_code, 200)
