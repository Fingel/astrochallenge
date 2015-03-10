from django.conf.urls import patterns, url, include
from django.views.generic.detail import DetailView


from astrochallenge.accounts import views
from astrochallenge.objects.models import Observation

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^accounts/profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^observations/(?P<slug>\d+)/$', DetailView.as_view(model=Observation, slug_field='pk'), name='observation-detail'),
    url(r'^equipment/add/$', views.add_equipment, name='add-equipment'),
    url(r'^equipment/delete/(?P<pk>\d+)/$', views.delete_equipment, name='delete-equipment'),

)
