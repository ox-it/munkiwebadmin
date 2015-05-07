from django.conf.urls import patterns, include, url

from inventory import views

urlpatterns = [
    url(r'^index/*$', views.index, name='inventory-views-index' ),
    url(r'^$', views.index),
    url(r'^submit/*$', views.submit),
    url(r'^hash/(?P<mac>[^/]+)$', views.inventory_hash),
    url(r'^detail/(?P<mac>[^/]+)$', views.detail),
    url(r'^items/*$', views.items, name='inventory-views-items'),
    url(r'^items.json/*$', views.items_json),
    #url(r'^(?P<mac>[^/]+)$', views.detail),
]
