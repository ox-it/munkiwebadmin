from django.conf.urls import include, url

from reports import views
   
urlpatterns = [
    url(r'^index/*$', views.index, name='reports-views-index'),
    url(r'^dashboard/*$', views.dashboard),
    url(r'^$', views.overview, name='reports-views-overview'),
    url(r'^overview/*$', views.overview),
    url(r'^detail/(?P<mac>[^/]+)$', views.detail),
    url(r'^raw/(?P<mac>[^/]+)$', views.raw),
    url(r'^submit/(?P<submission_type>[^/]+)$', views.submit),
    url(r'^warranty/(?P<serial>[^/]+)$', views.warranty),
    # for compatibilty with MunkiReport scripts
    url(r'^ip$', views.lookup_ip),
]

#urlpatterns = patterns('reports.views',
#    url(r'^index/*$', 'index'),
#    url(r'^dashboard/*$', 'dashboard'),
#    url(r'^$', 'overview'),
#    url(r'^overview/*$', 'overview'),
#    url(r'^detail/(?P<mac>[^/]+)$', 'detail'),
#    url(r'^raw/(?P<mac>[^/]+)$', 'raw'),
#    url(r'^submit/(?P<submission_type>[^/]+)$', 'submit'),
#    url(r'^warranty/(?P<serial>[^/]+)$', 'warranty'),
#    # for compatibilty with MunkiReport scripts
#    url(r'^ip$', 'lookup_ip'),
#    url(r'^(?P<submission_type>[^/]+)$', 'submit'),
#)
