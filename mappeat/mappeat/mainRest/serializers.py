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

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"  
"""
TODO: def create:
    Crear nuevo propietario creando un Usuario dentro del metodo create y asociando dicho
    propietario a este nuevo usuario
"""

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

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__" 
        
class Menu_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_Category
        fields = "__all__" 
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" 
        
class Ticket_ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Resume
        fields = "__all__"         

class Ticket_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Detail
        fields = "__all__"         

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"         
            
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"         
            
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"         
            

# ViewSets define the view behavior.
class MesureUnityViewSet(viewsets.ModelViewSet):
    queryset = Mesure_Unity.objects.all()
    serializer_class = MesureUnitySerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    
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
    
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer 
    
class Menu_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Menu_Category.objects.all()
    serializer_class = Menu_CategorySerializer    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  
    
class Ticket_ResumeViewSet(viewsets.ModelViewSet):
    queryset = Ticket_Resume.objects.all()
    serializer_class = Ticket_ResumeSerializer 
    
class Ticket_DetailViewSet(viewsets.ModelViewSet):
    queryset = Ticket_Detail.objects.all()
    serializer_class = Ticket_DetailSerializer  
    
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer  

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer  

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Ticket_Detail.objects.all()
    serializer_class = Ticket_DetailSerializer  

    
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'mesureUnities', MesureUnityViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'suply_categories', Supply_CategoryViewSet)
router.register(r'suplies', SupplyViewSet)
router.register(r'ref_staff_roles', Ref_Staff_RolViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'tables', TableViewSet)
router.register(r'menu_categories', Menu_CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'ticket_resumes', Ticket_ResumeViewSet)
router.register(r'ticket_details', Ticket_DetailViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'inventory', InventoryViewSet)
















