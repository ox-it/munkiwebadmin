from django.conf.urls import patterns, include, url

from licenses import views

urlpatterns = [
    url(r'^$', views.index, name='licenses-views-index'),
    url(r'^available/$', views.available),
    url(r'^available/(?P<item_name>[^/]+)$', views.available),
    url(r'^usage/$', views.usage),
    url(r'^usage/(?P<item_name>[^/]+)$', views.usage),
]
