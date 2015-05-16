
from django.conf.urls import patterns, include, url

from jssmanifests import xmlviews

urlpatterns = [
    url(r'^xml/(?P<manifest_name>[^/]+)/?$', xmlviews.manifest,
                                                  name='xml-manifest'),
]
