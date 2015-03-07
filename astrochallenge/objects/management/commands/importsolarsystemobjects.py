from django.core.management.base import BaseCommand
from astrochallenge.objects.models import SolarSystemObject
from decimal import *


class Command(BaseCommand):
    args = '<file>'
    help = "Import messier catalog items"

    def handle(self, *args, **options):
        ss_objects = []
        sun = SolarSystemObject(
            index=0,
            name="Sun",
            type="ST",
            ephemeride="pyephem:Sun",
            description="Our star, the Sun.",
            mass=333000,
            mass_unit="e",
            points=100,
            image="ss_objects/sun.jpg"
        )
        sun.save()

        mercury = SolarSystemObject(
            index=1,
            name="Mercury",
            type="P",
            ephemeride="pyephem:Mercury",
            description="The first of 8 planets in our solar system",
            mass=0.055,
            mass_unit="e",
            points=75,
            parent=sun,
            image="ss_objects/mercury.jpg"
        )
        mercury.save()

        venus = SolarSystemObject(
            index=2,
            name="Venus",
            type="P",
            ephemeride="pyephem:Venus",
            description="The second planet",
            mass=0.815,
            mass_unit="e",
            points=100,
            parent=sun,
            image="ss_objects/venus.jpg"
        )
        venus.save()

        earth = SolarSystemObject(
            index=3,
            name="Earth",
            type="P",
            ephemeride="",
            description="Our home planet",
            mass=1,
            mass_unit="e",
            points=0,
            parent=sun,
            image="ss_objects/earth.jpg"
        )
        earth.save()

        mars = SolarSystemObject(
            index=4,
            name="Mars",
            type="P",
            ephemeride="pyephem:Mars",
            description="The red planet",
            mass=0.107,
            mass_unit="e",
            points=100,
            parent=sun,
            image="ss_objects/mars.jpg"
        )
        mars.save()

        jupiter = SolarSystemObject(
            index=5,
            name="Jupiter",
            type="P",
            ephemeride="pyephem:Jupiter",
            description="The largest planet",
            mass=317.8,
            mass_unit="e",
            points=100,
            parent=sun,
            image="ss_objects/jupiter.jpg"
        )
        jupiter.save()

        saturn = SolarSystemObject(
            index=6,
            name="Saturn",
            type="P",
            ephemeride="pyephem:Saturn",
            description="The ringed",
            mass=95.152,
            mass_unit="e",
            points=100,
            parent=sun,
            image="ss_objects/saturn.jpg"
        )
        saturn.save()

        uranus = SolarSystemObject(
            index=7,
            name="Uranus",
            type="P",
            ephemeride="pyephem:Uranus",
            description="The blue",
            mass=14.536,
            mass_unit="e",
            points=50,
            parent=sun,
            image="ss_objects/uranus.jpg"
        )
        uranus.save()

        neptune = SolarSystemObject(
            index=8,
            name="Neptune",
            type="P",
            ephemeride="pyephem:Neptune",
            description="The green",
            mass=17.147,
            mass_unit="e",
            points=50,
            parent=sun,
            image="ss_objects/neptune.jpg"
        )
        neptune.save()

        phobos = SolarSystemObject(
            index=9,
            name="Phobos",
            type="M",
            ephemeride="pyephem:Phobos",
            description="The larger of Mars' two moons. Phobos is named after the son of Ares and Venus and embodies horror. Due to tidal interactions Phobos is predicted to crash into the Martian surface in about 50 million years.",
            mass=1.0669E16,
            mass_unit="kg",
            points=1,
            parent=mars,
            image="ss_objects/phobos.jpg"
        )
        phobos.save()

        deimos = SolarSystemObject(
            index=10,
            name="Deimos",
            type="M",
            ephemeride="pyephem:Deimos",
            description="The smaller of Mars' two moons. Like Mars' other moon Phobos, Deimos is too small to achieve geostatic equilibrium as has an irregular shape. In Greek mythology Deimos was the son of Ares and Venus and the twin brother of Phobos and was the personification of Terror.",
            mass=1.4762E15,
            mass_unit="kg",
            points=1,
            parent=mars,
            image="ss_objects/deimos.jpg"
        )
        deimos.save()

        moon = SolarSystemObject(
            index=11,
            name="Moon",
            type="M",
            ephemeride="pyephem:Moon",
            description="",
            mass=7.3477E22,
            mass_unit="kg",
            points=100,
            parent=earth,
            image="ss_objects/moon.jpg"
        )
        moon.save()

        for ss_object in ss_objects:
            ss_object.save()
