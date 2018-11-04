from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='epgentity-list', permanent=False), name='index'),
    url(r'^api/update_data/$', views.update_data, name='update_data'),
    url(r'^api/channels/$', views.ChannelList.as_view(), name='channel-list'),
    url(r'^api/channels/(?P<pk>[0-9]+)$', views.ChannelDetail.as_view(), name='channel-detail'),
    url(r'^api/epgentities/$', views.EPGEntityList.as_view(), name='epgentity-list'),
    url(r'^api/epgentities/(?P<pk>[0-9]+)$', views.EPGEntityDetail.as_view(), name='epgentity-detail'),
    url(r'^api/genres/$', views.GenreList.as_view(), name='genre-list'),
    url(r'^api/genres/(?P<pk>[0-9]+)$', views.GenreDetail.as_view(), name='genre-detail'),
    url(r'^api/persones/$', views.PersonList.as_view(), name='person-list'),
    url(r'^api/persones/(?P<pk>[0-9]+)$', views.PersonDetail.as_view(), name='person-detail'),
]
