from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'mappeat/home.html')