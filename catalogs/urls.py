from django.conf.urls import patterns, include, url

from catalogs import views

urlpatterns =[
    #url(r'^$', views.index),
    #url(r'^(?P<catalog_name>[^/]+)/$', views.detail),
    #url(r'^(?P<catalog_name>[^/]+)/(?P<item_index>\d+)/$', views.item_detail),
    #url(r'^(?P<catalog_name>[^/]+)/(?P<item_name>[^/]+)/$', views.detail),
    url(r'^$', views.catalog_view, name='catalogs-views-catalog_view'),
    url(r'^(?P<catalog_name>[^/]+)/$', views.catalog_view),
    url(r'^(?P<catalog_name>[^/]+)/(?P<item_index>\d+)/$', views.item_detail),
    #url(r'^(?P<catalog_name>[^/]+)/(?P<item_name>[^/]+)/$', views.test_index),
    #url(r'^(?P<catalog_name>[^/]+)/edit/$', views.edit),
]
