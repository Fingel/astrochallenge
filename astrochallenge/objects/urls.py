from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from astrochallenge.objects.models import Constellation, SolarSystemObject, Observation, Supernova
from astrochallenge.objects.views import (DSODetailView, DSOListView, DSOListViewJson,
    SSODetailView, SSOListViewJson, ObservationDetailView, post_observation,
    delete_observation, post_finderchart, SNDetailView)

urlpatterns = patterns('',
    url(r'^objects/constellations/$', ListView.as_view(model=Constellation), name="constellation-list"),
    url(r'^objects/constellations/(?P<slug>\D+)/$', DetailView.as_view(model=Constellation, slug_field="abbreviation"), name='constellation-detail'),
    url(r'^objects/constellations/(?P<slug>\d+)/$', DetailView.as_view(model=Constellation, slug_field="pk"), name='constellation-detail'),
    url(r'^objects/dso/$', DSOListView.as_view(), name="astroobject-list"),
    url(r'^objects/dso/json$', DSOListViewJson.as_view(), name="astroobject-list-json"),
    url(r'^objects/dso/json/(?P<catalog>\D+)/$', DSOListViewJson.as_view(), name="astroobject-list-json"),
    url(r'^objects/dso/(?P<pk>\d+)/$', DSODetailView.as_view(), name="astroobject-detail"),
    url(r'^objects/dso/(?P<catalog>\w+)/(?P<designation>\d+)/$', DSODetailView.as_view(), name="astroobject-detail"),
    url(r'^objects/solarsystem/json/$', SSOListViewJson.as_view(), name="solarsystemobject-list-json"),
    url(r'^objects/solarsystem/$', ListView.as_view(model=SolarSystemObject), name="solarsystemobject-list"),
    url(r'^objects/solarsystem/(?P<slug>\D+)/$', SSODetailView.as_view(model=SolarSystemObject, slug_field="name"), name="solarsystemobject-detail"),
    url(r'^objects/solarsystem/(?P<slug>\d+)/$', SSODetailView.as_view(model=SolarSystemObject, slug_field="pk"), name="solarsystemobject-detail"),
    url(r'^objects/supernovae/(?P<slug>\D+)/$', SNDetailView.as_view(model=Supernova, slug_field="name"), name="supernova-detail"),
    url(r'^objects/supernovae/(?P<slug>\d+)/$', SNDetailView.as_view(model=Supernova, slug_field="pk"), name="supernova-detail"),
)

urlpatterns += patterns('',
    url(r'^observations/(?P<slug>\d+)/$', ObservationDetailView.as_view(model=Observation, slug_field='pk'), name='observation-detail'),
    url(r'^observation/choose/$', TemplateView.as_view(template_name="objects/choose.html"), name="choose-observation"),
    url(r'^observation/$', post_observation, name="post-observation"),
    url(r'^observation/(?P<observation_id>\d+)/delete/$', delete_observation, name="delete-observation"),
    url(r'^observation/(?P<observation_id>\d+)/edit/$', post_observation, name="edit-observation"),
)

urlpatterns += patterns('',
    url(r'^finderchart/$', post_finderchart, name="post-finderchart"),
)
