from django.conf.urls import patterns, url, include

from astrochallenge.accounts import views

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.ContactView.as_view(), name="contact"),
    url(r'^accounts/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^accounts/profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^equipment/add/$', views.add_equipment, name='add-equipment'),
    url(r'^equipment/delete/(?P<pk>\d+)/$', views.delete_equipment, name='delete-equipment'),
)
