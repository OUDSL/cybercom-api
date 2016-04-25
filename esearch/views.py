from django.shortcuts import render

# Create your views here.
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly,DjangoModelPermissionsOrAnonReadOnly,AllowAny
from rest_framework.views import APIView
#from cybercom_queue.ccelery.q import QueueTask, list_tasks, task_docstring
#from cybercom_queue.models import Run_model
from rest_framework.renderers import JSONRenderer, JSONPRenderer
#from renderer import QueueRunBrowsableAPIRenderer
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
#from cybercom_queue.util import trim
#from rest_framework.authtoken.models import Token
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator
#task = list_tasks()['available_tasks']
#from rest_framework.viewsets import ModelViewSet
#from serializer import FileUploadSerializer
import os

from elasticsearch import Elasticsearch

from esearch.elastic_search import es_get, es_search
from esearch.es_config import ES_HOST

class es_search_view(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #model = Run_model
    #parser_classes = (JSONParser,MultiPartParser,FormParser)
    #renderer_classes = (QueueRunBrowsableAPIRenderer, JSONRenderer, JSONPRenderer,)
    def __init__(self):
        self.es = Elasticsearch(ES_HOST)

    def get(self, request, index=None, doctype=None, format=None):
	
        query = request.QUERY_PARAMS.get('query', None)
        page_size = request.QUERY_PARAMS.get(api_settings.user_settings.get('PAGINATE_BY_PARAM', 'page_size'),
                                             api_settings.user_settings.get('PAGINATE_BY', 10))
        try:
            page = int(request.QUERY_PARAMS.get('page', 1))
        except:
            page = 1
        try:
            page_size = int(request.QUERY_PARAMS.get('page_size', page_size))
        except:
            page_size = int(api_settings.user_settings.get('PAGINATE_BY', 10))

        #url = request and request.build_absolute_uri() or ''
        action = request.QUERY_PARAMS.get('esaction','None')
	print action
        if action.lower()=="mget":
            ids = request.QUERY_PARAMS.get('ids',None)
            if ids:
                data = es_get(self.es, index,doctype, ids.split(','))
            else:
                data = {"ERROR":"Must provide comma separated 'ids' query param"}
        else:
            data = es_search(self.es, index, doctype, query=query, page=page, nPerPage=page_size) #, uri=url)
        return Response(data)

#def es_get(es_client, index, doc_type, ids=[]):
#def es_search(es_client, index, doc_type, query=None, page=1, nPerPage=10): #, uri=''):
