from django.conf.urls import url, include
from . import views
from . import serializers

app_name = 'mainRest'
urlpatterns = [
    # Examples:
    # url(r'^$', 'beermenu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Index
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/', include(serializers.router.urls)),

]