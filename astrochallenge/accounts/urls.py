from django.conf.urls import patterns, url, include
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from astrochallenge.accounts import views
from django.contrib.auth.models import User

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.ContactView.as_view(), name="contact"),
    url(r'^accounts/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/profile/(?P<username>.+)/$', views.profile, name='profile'),
    url(r'^equipment/add/$', views.add_equipment, name='add-equipment'),
    url(r'^equipment/delete/(?P<pk>\d+)/$', views.delete_equipment, name='delete-equipment'),
    url(r'^equipment/$', views.list_equipment, name='list-equipment'),
    url(r'^accounts/kudos/(?P<observation>\d+)/$', views.give_kudos, name='give-kudos'),
    url(r'^accounts/users/$', ListView.as_view(model=User, template_name="accounts/user_list.html"), name='user-list'),
    url(r'^faq/$', TemplateView.as_view(template_name="accounts/faq.html"), name="faq"),
    url(r'^comment/delete/(?P<pk>\d+)/$', views.delete_comment, name='delete-comment'),
)
