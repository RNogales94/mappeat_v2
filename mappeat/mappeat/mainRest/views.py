
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

from .models import *

def index(request):
    return render(request, 'mainRest/index.html')

def prueba_api(request):
    return render(request, 'mainRest/prueba_api.html')

def prueba_gui(request):
    return render(request, 'mainRest/prueba_gui.html')