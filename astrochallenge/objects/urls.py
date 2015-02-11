from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from astrochallenge.objects.models import Constellation

urlpatterns = patterns('',
    url(r'^objects/$', TemplateView.as_view(template_name="objects/index.html"), name="object-index"),
    url(r'^objects/constellations/$', ListView.as_view(model=Constellation), name="constellation-list"),
    url(r'^objects/constellations/(?P<slug>\w+)/$', DetailView.as_view(model=Constellation, slug_field="abbreviation"), name='constellation-detail'),

)
