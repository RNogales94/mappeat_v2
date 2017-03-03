from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from .models import *

class TableResource(ModelResource):
    """
    API Facet
    """
    class Meta:
        queryset = Table.objects.all()
        resource_name = 'table'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True