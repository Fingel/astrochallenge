from django.conf.urls import patterns, url

from astrochallenge.accounts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
