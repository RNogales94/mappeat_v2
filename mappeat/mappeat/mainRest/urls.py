from django.conf.urls import url, include
from . import views
from . import serializers
app_name = 'mainRest'
urlpatterns = [
    # Index
#    url(r'^$', views.index, name='index'),
    url(r'^$', views.mappeatlogin, name='login'),
    url(r'^api/v1/', include(serializers.router.urls)),
]
