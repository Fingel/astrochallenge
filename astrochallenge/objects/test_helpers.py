from models import AstroObject, SolarSystemObject, Constellation, Observation, CatalogObject, Supernova, SupernovaMagnitude
from factory.fuzzy import FuzzyText, FuzzyChoice, FuzzyFloat, FuzzyInteger, FuzzyDate, FuzzyDateTime
from astrochallenge.accounts.test_helpers import UserProfileFactory, EquipmentFactory
from django.conf import settings
from django.utils import timezone
import factory
import datetime


class ConstellationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Constellation

    abbreviation = FuzzyText(length=3)
    latin_name = FuzzyText(length=10)
    english_name = FuzzyText(length=30)
    latin_genitive = FuzzyText(length=10)
    image = None


class AstroObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AstroObject

    type = FuzzyChoice(choices=[u'Asterism',
                                u'Double Star',
                                u'Galaxy',
                                u'Globular Cluster',
                                u'Nebula',
                                u'Nebulosity in External Galaxy',
                                u'Open Cluster',
                                u'Planetary Nebula',
                                u'Star',
                                u'Supernova Remnant',
                                u'Triple Star'])
    index = factory.Sequence(lambda n: n)
    ra_hours = FuzzyFloat(0.0, 23.0)
    ra_minutes = FuzzyFloat(0.0, 59.0)
    ra_seconds = FuzzyFloat(0.0, 59.0)
    dec_sign = FuzzyChoice(choices=['+', '-'])
    dec_deg = FuzzyInteger(0, 89)
    dec_min = FuzzyFloat(0.0, 59.0)
    dec_seconds = FuzzyFloat(0.0, 59)
    magnitude = FuzzyFloat(-4.0, 14)
    size = FuzzyFloat(0.1, 10000.0)
    distance = FuzzyInteger(1, 1000000000)
    details = FuzzyText(length=40)
    description = FuzzyText(length=500)
    common_name = factory.Sequence(lambda n: "NGC{0}".format(n))
    points = FuzzyInteger(0, 100)
    image = None
    image_attribution = FuzzyText(length=50)
    discoverer = FuzzyText(length=20)
    discovery_date = FuzzyDate(start_date=datetime.date(1700, 1, 1))

    constellation = factory.SubFactory(ConstellationFactory)


class SupernovaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supernova

    sntype = FuzzyChoice(choices=[u'Ia', u'II', u'IIb'])
    ra_hours = FuzzyFloat(0.0, 23.0)
    ra_minutes = FuzzyFloat(0.0, 59.0)
    ra_seconds = FuzzyFloat(0.0, 59.0)
    dec_sign = FuzzyChoice(choices=['+', '-'])
    dec_deg = FuzzyInteger(0, 89)
    dec_min = FuzzyFloat(0.0, 59.0)
    dec_seconds = FuzzyFloat(0.0, 59)
    z = FuzzyFloat(0, 0.5)
    name = factory.Sequence(lambda n: "SN/{0}".format(n))
    points = FuzzyInteger(0, 100)
    date_added = timezone.now()
    discovery_date = FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=29),
        end_dt=timezone.now()
    )

    astro_object = factory.SubFactory(AstroObjectFactory)


class SupernovaMagnitudeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SupernovaMagnitude

    magnitude = FuzzyFloat(-2.0, 4.0)
    time = FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=29),
        end_dt=timezone.now()
    )

    supernova = factory.SubFactory(SupernovaFactory)


class SolarSystemObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SolarSystemObject

    name = FuzzyChoice(choices=['Juipter', 'Mars', 'Saturn'])
    type = FuzzyChoice(choices=settings.SOLAR_SYSTEM_OBJECT_TYPES)
    index = factory.Sequence(lambda n: n)
    description = FuzzyText(length=500)
    mass = FuzzyFloat(1, 10000)
    mass_unit = FuzzyChoice(choices=['s', 'e', 'j', 'kg'])
    points = FuzzyInteger(0, 100)
    image = None
    image_attribution = FuzzyText(length=50)


class ObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Observation
        abstract = True

    date = FuzzyDate(start_date=datetime.date(2015, 1, 1))
    points_earned = FuzzyInteger(0, 100)
    lat = FuzzyFloat(-90, 90)
    lng = FuzzyFloat(-180, 180)
    seeing = FuzzyChoice(choices=['P', 'BA', 'A', 'AA', 'E'])
    light_pollution = FuzzyChoice(choices=['P', 'BA', 'A', 'AA', 'E'])
    description = FuzzyText(length=200)
    featured = FuzzyChoice(choices=[True, False])

    equipment = factory.SubFactory(EquipmentFactory)
    user_profile = factory.SubFactory(UserProfileFactory)


class AstroObjectObservationFactory(ObservationFactory):
    content_object = factory.SubFactory(AstroObjectFactory)


class SolarSystemObjectObservationFactory(ObservationFactory):
    content_object = factory.SubFactory(SolarSystemObjectFactory)


class CatalogObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CatalogObject

    astro_object = factory.SubFactory(AstroObjectFactory)
    catalog = FuzzyChoice(choices=settings.CATALOGS.keys())
    designation = FuzzyInteger(0, 10000)
