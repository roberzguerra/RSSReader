from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import os

from rss_reader.views import HomePageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RSSReader.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^(?P<page_number>\d+)/$', HomePageView.as_view(), name="home-page"),
)
