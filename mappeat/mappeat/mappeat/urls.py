"""mappeat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views


#from rest_framework.documentation import include_docs_urls #Default DOC
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Mappeat Swagger API')

#Recuperar contraseña y demás cosas de /accounts
from django.contrib.auth.views import password_reset, password_reset_done, \
                                password_reset_confirm, password_reset_complete


app_name = 'mappeat'
urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^mainRest/', include('mainRest.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^dev/docs/', schema_view),
    url(r'^accounts_api/', include('registration_api.urls')),

    #accounts section:
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/password/reset/$', password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', password_reset_done),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
     {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', password_reset_complete),
]

"""
Seccion para herramienta de DEBUG:
"""
from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
