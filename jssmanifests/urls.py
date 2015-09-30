from django.conf.urls import patterns, include, url

from jssmanifests import xmlviews, views, testviews

urlpatterns = patterns ('jssmanifests.views',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.JSSComputerAttributeMappingDetail.as_view(), 
      name='detail'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.JSSComputerAttributeMappingUpdate.as_view(), 
      name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.JSSComputerAttributeMappingDelete.as_view(), 
      name='delete'),
    url(r'^toggle-enabled/(?P<pk>[0-9]+)/$', views.toggle_enabled, name='toggle-enabled'),
    url(r'^testindex$', testviews.index),
    url(r'^xml/(?P<manifest_name>[^/]+)/?$', xmlviews.manifest,
                                                  name='xml-manifest'),
)


