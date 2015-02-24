from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from astrochallenge.objects.models import Constellation, SolarSystemObject
from astrochallenge.objects.views import DSODetailView, DSOListView, DSOListViewJson, post_observation, delete_observation

urlpatterns = patterns('',
    url(r'^objects/$', TemplateView.as_view(template_name="objects/index.html"), name="object-index"),
    url(r'^objects/constellations/$', ListView.as_view(model=Constellation), name="constellation-list"),
    url(r'^objects/constellations/(?P<slug>\D+)/$', DetailView.as_view(model=Constellation, slug_field="abbreviation"), name='constellation-detail'),
    url(r'^objects/constellations/(?P<slug>\d+)/$', DetailView.as_view(model=Constellation, slug_field="pk"), name='constellation-detail'),
    url(r'^objects/dso/$', DSOListView.as_view(), name="astroobject-list"),
    url(r'^objects/dso/json$', DSOListViewJson.as_view(), name="astroobject-list-json"),
    url(r'^objects/dso/json/(?P<catalog>\D+)/$', DSOListViewJson.as_view(), name="astroobject-list-json"),
    url(r'^objects/dso/(?P<pk>\d+)/$', DSODetailView.as_view(), name="astroobject-detail"),
    url(r'^objects/dso/(?P<catalog>\w+)/(?P<designation>\d+)/$', DSODetailView.as_view(), name="astroobject-detail"),
    url(r'^objects/solarsystem/$', ListView.as_view(model=SolarSystemObject), name="solarsystemobject-list")
)

urlpatterns += patterns('',
    url(r'^observation/$', post_observation, name="post-observation"),
    url(r'^observation/(?P<observation_id>\d+)/delete/$', delete_observation, name="delete-observation")
    )
