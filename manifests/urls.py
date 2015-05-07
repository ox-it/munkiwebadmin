from django.conf.urls import patterns, include, url

from manifests import views

urlpatterns = [
    url(r'^$', views.index, name='manifests-views-index'),
    url(r'^new$', views.new, name='manifests-views-new'),
    url(r'^delete/(?P<manifest_name>[^/]+)/$', views.delete),
    #url(r'^#(?P<manifest_name>.+)/$', views.index),
    url(r'^view/(?P<manifest_name>[^/]+)/$', views.view),
    url(r'^detail/(?P<manifest_name>[^/]+)$', views.detail),
]
