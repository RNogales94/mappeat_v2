
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

from .models import *
from .forms import TableForm
from django.views.generic import TemplateView


# Create your views here.
class TableFormView(TemplateView):
    template_name = "mainRest/tables/new.html"

    def get_context_data(self, **kwargs):
        context = super(TableFormView, self).get_context_data(**kwargs)
        context.update(TableForm=TableForm())
        return context

    

# Shows the tables' list.
def index(request):
    table_list = Table.objects.order_by('type_table', 'number')
    context = {'table_list': table_list}
    return render(request, 'mainRest/index.html', context)

#TODO
def detailActualMeal(request, meal_id, table_id):
    return render(request, 'mainRest/actual.html', context)

#TODO
def addDish(request, meal_id):
    return render(request)



#Ancilary views:

#TODO
#def addStaff(request):
#    return render(request, 'mainRest/addStaf.html')



