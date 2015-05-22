from models import CustomComment
from astrochallenge.accounts.test_helpers import UserFactory
from astrochallenge.objects.test_helpers import AstroObjectObservationFactory
from factory.fuzzy import FuzzyText
import factory


class CustomCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomComment

    comment = FuzzyText(length=200)

    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(AstroObjectObservationFactory)
    site_id = 1
