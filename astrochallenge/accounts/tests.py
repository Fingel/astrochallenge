from test_helpers import UserFactory
from django.test import TransactionTestCase
from models import Equipment


class AccountsModelTests(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_user_profile(self):
        self.assertEqual(str(self.user.userprofile), self.user.username)
        self.assertEqual(0, self.user.userprofile.points)
        self.assertIsNotNone(self.user.userprofile.observer)
        self.assertIsNotNone(self.user.userprofile.sunset)

        Equipment(instrument="test equipment", user_profile=self.user.userprofile).save()
        self.assertEqual(1, len(self.user.userprofile.equipment_set.all()))
