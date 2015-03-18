from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView

from astrochallenge.challenges.models import Challenge
from astrochallenge.challenges.views import ChallengeListView

urlpatterns = patterns('',
    url(r'^challenges/$', ChallengeListView.as_view(model=Challenge), name="challenge-list"),
    url(r'^challenges/(?P<slug>\d+)/$', DetailView.as_view(model=Challenge, slug_field="pk"), name="challenge-detail"),
)
