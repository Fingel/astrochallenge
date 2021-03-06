from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from sitemap import *


def required(wrapping_functions, patterns_rslt):
    if not hasattr(wrapping_functions, '__iter__'):
        wrapping_functions = (wrapping_functions,)

    return [
        _wrap_instance__resolve(wrapping_functions, instance)
        for instance in patterns_rslt
    ]


def _wrap_instance__resolve(wrapping_functions, instance):
    if not hasattr(instance, 'resolve'):
        return instance
    resolve = getattr(instance, 'resolve')

    def _wrap_func_in_returned_resolver_match(*args, **kwargs):
        rslt = resolve(*args, **kwargs)

        if not hasattr(rslt, 'func'):
            return rslt
        f = getattr(rslt, 'func')

        for _f in reversed(wrapping_functions):
            # @decorate the function from inner to outter
            f = _f(f)

        setattr(rslt, 'func', f)

        return rslt

    setattr(instance, 'resolve', _wrap_func_in_returned_resolver_match)

    return instance

sitemaps = {
    'AstroObjectSitemap': AstroObjectSitemap,
    'SolarSystemObjectSitemap': SolarSystemObjectSitemap,
    'ObservationSitemap': ObservationSitemap,
    'ConstellationSitemap': ConstellationSitemap,
    'ChallengeSitemap': ChallengeSitemap,
    'SupernovaSitemap': SupernovaSitemap,
    'StaticViewsSitemap': StaticViewsSitemap,
}

urlpatterns = patterns('',
    url('^markdown/', include('django_markdown.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^', include('astrochallenge.accounts.urls')),
    url(r'^', include('astrochallenge.objects.urls')),
    url(r'^', include('astrochallenge.challenges.urls')),
    url(r'^redrock/', include(admin.site.urls)),
    url(r'sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)

urlpatterns += required(
    login_required,
    patterns('',
        (r'^comments/', include('django_comments.urls')),
    )
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
