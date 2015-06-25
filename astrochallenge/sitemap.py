from django.contrib.sitemaps import Sitemap
from objects.models import AstroObject, SolarSystemObject, Constellation, Observation, Supernova
from challenges.models import Challenge
from django.core.urlresolvers import reverse


class AstroObjectSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return AstroObject.objects.all()


class SolarSystemObjectSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return SolarSystemObject.objects.all()


class SupernovaSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return Supernova.objects.all()


class ObservationSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return Observation.objects.all()


class ConstellationSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Constellation.objects.all()


class ChallengeSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Challenge.objects.all()


class StaticViewsSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return ['index', 'contact', 'user-list', 'faq', 'challenge-list']

    def location(self, item):
        return reverse(item)
