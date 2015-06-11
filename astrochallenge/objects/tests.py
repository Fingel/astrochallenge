from test_helpers import SolarSystemObjectFactory
from astrochallenge.accounts.test_helpers import UserProfileFactory
from django.test import TransactionTestCase

import datetime


class ObjectModeltests(TransactionTestCase):
    def test_solarsystemobject(self):
        user_profile = UserProfileFactory.create()
        solarsystemobject = SolarSystemObjectFactory.create(
            ephemeride='pyephem:Venus',
            type='P'
        )
        self.assertTrue('elongation' in solarsystemobject.general_info.keys())
        self.assertTrue('up' in solarsystemobject.observation_info(user_profile.observer))

        solarsystemobject = SolarSystemObjectFactory.create(
            ephemeride='pyephem:Phobos',
            type='M'
        )
        self.assertTrue('earth_visible' in solarsystemobject.general_info.keys())
        self.assertIsNotNone(solarsystemobject.ra)
        self.assertIsNotNone(solarsystemobject.dec)
        self.assertIsNotNone(solarsystemobject.ra_dec_on_date(datetime.date.today()))
