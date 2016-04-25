__author__ = 'mstacy'
from django.conf.urls import patterns, url
from esearch.views import es_search_view 
from rest_framework.urlpatterns import format_suffix_patterns
from api import config

urlpatterns = patterns('',
                       #url(r'^data/$', MongoDataStore.as_view(), name='data-list'),
                       #url(r'^data/(?P<database>[^/]+)/$', MongoDataStore.as_view(), name='data-list'),
                       url(r'^data/(?P<index>[^/]+)/(?P<doc_type>[^/]+)/$', es_search_view.as_view(),name='es-detail'),
                       #url(r'^data/(?P<database>[^/]+)/(?P<collection>[^/]+)/(?P<id>[^/]+)/$', DataStoreDetail.as_view(),
                       #    name='data-detail-id'),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
