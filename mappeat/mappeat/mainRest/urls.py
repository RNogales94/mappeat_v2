from django.conf.urls import url, include
from . import views
from . import serializers

app_name = 'mainRest'
urlpatterns = [
    # Index
    url(r'^$', views.index, name='index'),
    url(r'^prueba_api$', views.prueba_api, name='prueba_api'),
    url(r'^prueba_gui$', views.prueba_gui, name='prueba_gui'),
    url(r'^prueba_acceso$', views.prueba_acceso, name='prueba_acceso'),
    url(r'^api/v1/', include(serializers.router.urls)),
]