from django.conf.urls import patterns, url, include

from astrochallenge.accounts import views

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^accounts/profile/(?P<username>\w+)/$', views.profile, name='profile'),

)
