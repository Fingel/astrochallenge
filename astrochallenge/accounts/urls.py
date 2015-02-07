from django.conf.urls import patterns, url

from astrochallenge.accounts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
    url(r'^accounts/profile/$', views.profile, name='profile'),

)
