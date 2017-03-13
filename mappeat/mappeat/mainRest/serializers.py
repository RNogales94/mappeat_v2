"""
Serializers
"""

from rest_framework import routers, serializers, viewsets
from .models import *

"""
from django.contrib.auth.models import User

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
"""


"""
Serializadores para los modelos de mainRest
"""
# Serializers define the API representation.
class MesureUnitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mesure_Unity
        fields = ('name', 'simbol')

# ViewSets define the view behavior.
class MesureUnityViewSet(viewsets.ModelViewSet):
    queryset = Mesure_Unity.objects.all()
    serializer_class = MesureUnitySerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'mesureUnities', MesureUnityViewSet)



















