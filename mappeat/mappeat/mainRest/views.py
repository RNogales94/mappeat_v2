
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

from .models import *

# PROVISIONAL: index en el futuro mostrará la single page app
# Shows the tables' list.
def index(request):
    table_list = Table.objects.order_by('type_table', 'number')
    context = {'table_list': table_list}
    return render(request, 'mainRest/index.html', context)

def prueba_api(request):
    return render(request, 'mainRest/prueba_api.html')