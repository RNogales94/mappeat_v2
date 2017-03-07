from django.conf.urls import url
from . import views

app_name = 'mainRest'
urlpatterns = [
    # Examples:
    # url(r'^$', 'beermenu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Index
    url(r'^$', views.index, name='index'),
]