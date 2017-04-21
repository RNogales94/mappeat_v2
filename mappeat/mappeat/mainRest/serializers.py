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
class MesureUnitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure_Unity
        fields = ('name', 'simbol')

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        #fields = ('owner', 'name', 'address', 'city')    
        fields = "__all__" 
        
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__" 
        
class Supply_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply_Category
        fields = "__all__" 
        
class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"    

class Ref_Staff_RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref_Staff_Rol
        fields = "__all__"   

class StaffSerializer(serializers.ModelSerializer):
    staff_role_code = Ref_Staff_RolSerializer()
    class Meta:
        model = Staff
        fields = ('staff_role_code', 'first_name', 'last_name') 
    
    def create(self, validated_data):
        print(validated_data)
        rol_data = validated_data.pop('staff_role_code')
        rol_choice = rol_data['staf_role_description']
        rol = Ref_Staff_Rol.objects.all().filter(staf_role_description=rol_choice)
        staff = Staff.objects.create(staff_role_code=rol[0], **validated_data)
        return staff
        
        
        
# ViewSets define the view behavior.
class MesureUnityViewSet(viewsets.ModelViewSet):
    queryset = Mesure_Unity.objects.all()
    serializer_class = MesureUnitySerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer    
    
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer      
    
class Supply_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Supply_Category.objects.all()
    serializer_class = Supply_CategorySerializer    
    
class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer   
    
class Ref_Staff_RolViewSet(viewsets.ModelViewSet):
    queryset = Ref_Staff_Rol.objects.all()
    serializer_class = Ref_Staff_RolSerializer
    
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer 
    
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'mesureUnities', MesureUnityViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'suply_categories', Supply_CategoryViewSet)
router.register(r'suplies', SupplyViewSet)
router.register(r'ref_staff_roles', Ref_Staff_RolViewSet)
router.register(r'staff', StaffViewSet)




















