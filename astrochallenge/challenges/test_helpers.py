from factory.fuzzy import FuzzyText, FuzzyChoice, FuzzyInteger, FuzzyDateTime
from models import Challenge
from django.conf import settings
from pytz import UTC
import factory
import datetime


class ChallengeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Challenge

    target = FuzzyChoice(choices=settings.CHALLENGE_TYPES)
    type = FuzzyChoice(choices=('set', 'numeric'))
    name = FuzzyText(length=50)
    description = FuzzyText(length=1000)
    rating = FuzzyInteger(0, 5)
    number = FuzzyInteger(0, 50)
    multiplier = FuzzyInteger(1, 5)
    bonus = FuzzyInteger(0, 200)
    complete_bonus = FuzzyInteger(0, 1000)
    start_time = FuzzyDateTime(datetime.datetime.now().replace(tzinfo=UTC))
    end_time = FuzzyDateTime(
        start_dt=datetime.datetime(2099, 1, 1, tzinfo=UTC),
        end_dt=datetime.datetime(2199, 1, 1, tzinfo=UTC))
    index = FuzzyInteger(0, 9999)
    image = None

    @factory.post_generation
    def solarsystemobjects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for solarsystemobject in extracted:
                self.solarsystemobjects.add(solarsystemobject)

    @factory.post_generation
    def astroobjects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for astroobject in extracted:
                self.astroobjects.add(astroobject)
