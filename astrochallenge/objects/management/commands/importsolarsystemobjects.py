from django.core.management.base import BaseCommand
from astrochallenge.objects.models import SolarSystemObject
from django.conf import settings
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

        moon = SolarSystemObject(
            index=9,
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

        phobos = SolarSystemObject(
            index=10,
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
            index=11,
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

        titan = SolarSystemObject(
            index=12,
            name="Titan",
            type="M",
            ephemeride="pyephem:Titan",
            description="Titan is Saturn's largest moon. It has a dense atmosphere and surface liquid in the form of liquid methane. Titan is the only body outside of earth that is known to have active hydrology.",
            mass=0.0225,
            mass_unit="e",
            points=50,
            parent=saturn,
            image="ss_objects/titan.jpg"
        )
        titan.save()

        enceladus = SolarSystemObject(
            index=12,
            name="Enceladus",
            type="M",
            ephemeride="pyephem:Enceladus",
            description="",
            mass=1.080E20,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/enceladus.jpg"
        )
        enceladus.save()

        mimas = SolarSystemObject(
            index=12,
            name="Mimas",
            type="M",
            ephemeride="pyephem:Mimas",
            description="",
            mass=3.7493E19,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/mimas.jpg"
        )
        mimas.save()

        rhea = SolarSystemObject(
            index=12,
            name="Rhea",
            type="M",
            ephemeride="pyephem:Rhea",
            description="",
            mass=2.306E21,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/rhea.jpg"
        )
        rhea.save()

        iapetus = SolarSystemObject(
            index=12,
            name="Iapetus",
            type="M",
            ephemeride="pyephem:Iapetus",
            description="",
            mass=1.805E21,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/iapetus.jpg"
        )
        iapetus.save()

        dione = SolarSystemObject(
            index=12,
            name="Dione",
            type="M",
            ephemeride="pyephem:Dione",
            description="",
            mass=1.095E21,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/dione.jpg"
        )
        dione.save()

        tethys = SolarSystemObject(
            index=12,
            name="Tethys",
            type="M",
            ephemeride="pyephem:Tethys",
            description="",
            mass=6.174E20,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/tethys.jpg"
        )
        tethys.save()

        hyperion = SolarSystemObject(
            index=12,
            name="Hyperion",
            type="M",
            ephemeride="pyephem:Hyperion",
            description="",
            mass=5.6199E18,
            mass_unit="kg",
            points=1,
            parent=saturn,
            image="ss_objects/hyperion.jpg"
        )
        hyperion.save()

        #  Jupiter

        europa = SolarSystemObject(
            index=13,
            name="Europa",
            type="M",
            ephemeride="pyephem:Europa",
            description="",
            mass=0.008,
            mass_unit="e",
            points=50,
            parent=jupiter,
            image="ss_objects/europa.jpg"
        )
        europa.save()

        io = SolarSystemObject(
            index=13,
            name="Io",
            type="M",
            ephemeride="pyephem:Io",
            description="",
            mass=0.015,
            mass_unit="e",
            points=50,
            parent=jupiter,
            image="ss_objects/io.jpg"
        )
        io.save()

        ganymede = SolarSystemObject(
            index=13,
            name="Ganymede",
            type="M",
            ephemeride="pyephem:Ganymede",
            description="",
            mass=0.025,
            mass_unit="e",
            points=50,
            parent=jupiter,
            image="ss_objects/ganymede.jpg"
        )
        ganymede.save()

        callisto = SolarSystemObject(
            index=13,
            name="Callisto",
            type="M",
            ephemeride="pyephem:Callisto",
            description="",
            mass=0.018,
            mass_unit="e",
            points=1,
            parent=jupiter,
            image="ss_objects/callisto.jpg"
        )
        callisto.save()

        #  Uranus

        miranda = SolarSystemObject(
            index=14,
            name="Miranda",
            type="M",
            ephemeride="pyephem:Miranda",
            description="",
            mass=6.59E19,
            mass_unit="kg",
            points=1,
            parent=uranus,
            image="ss_objects/miranda.jpg"
        )
        miranda.save()

        titania = SolarSystemObject(
            index=14,
            name="Titania",
            type="M",
            ephemeride="pyephem:Titania",
            description="",
            mass=3.527E21,
            mass_unit="kg",
            points=1,
            parent=uranus,
            image="ss_objects/titania.jpg"
        )
        titania.save()

        umbriel = SolarSystemObject(
            index=14,
            name="Umbriel",
            type="M",
            ephemeride="pyephem:Umbriel",
            description="",
            mass=1.172E21,
            mass_unit="kg",
            points=1,
            parent=uranus,
            image="ss_objects/umbriel.jpg"
        )
        umbriel.save()

        oberon = SolarSystemObject(
            index=14,
            name="Oberon",
            type="M",
            ephemeride="pyephem:Oberon",
            description="",
            mass=3.014E21,
            mass_unit="kg",
            points=1,
            parent=uranus,
            image="ss_objects/oberon.jpg"
        )
        oberon.save()

        ariel = SolarSystemObject(
            index=14,
            name="Ariel",
            type="M",
            ephemeride="pyephem:Ariel",
            description="",
            mass=1.353E21,
            mass_unit="kg",
            points=1,
            parent=uranus,
            image="ss_objects/ariel.jpg"
        )
        ariel.save()

        #  Neptune

        triton = SolarSystemObject(
            index=15,
            name="Triton",
            type="M",
            ephemeride="pyephem:Neptune",
            description="",
            mass=2.14E22,
            mass_unit="kg",
            points=1,
            parent=neptune,
            image="ss_objects/triton.jpg"
        )
        triton.save()

        pluto = SolarSystemObject(
            index=16,
            name="Pluto",
            type="DP",
            ephemeride="pyephem:Pluto",
            description="",
            mass=0.002,
            mass_unit="e",
            points=1,
            parent=sun,
            image="ss_objects/pluto.jpg"
        )
        pluto.save()

        #  Minor planets

        soft03bright = open(settings.PROJECT_ROOT + '/data/Soft03Bright.txt', 'r')
        for line in soft03bright:
            if line[0] == '#':
                pass
            else:
                ss_object = SolarSystemObject(
                    index=999999,
                    name=line.split(',')[0],
                    type='DP',
                    ephemeride=line,
                    points=1,
                    parent=sun
                )
                ss_objects.append(ss_object)
        #  Comets. Soft03Cmt.txt for full list, newcomets.txt for new
        comets = open(settings.PROJECT_ROOT + '/data/newcomets.txt', 'r')
        for line in comets:
            if line[0] == '#':
                pass
            else:
                ss_object = SolarSystemObject(
                    index=999999,
                    name=line.split(',')[0],
                    type='C',
                    ephemeride=line,
                    points=1,
                    parent=sun
                )
                ss_objects.append(ss_object)
        for ss_object in ss_objects:
            ss_object.save()
