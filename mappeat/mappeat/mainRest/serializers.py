"""
Serializers
"""

from rest_framework import routers, serializers, viewsets
from django_filters import rest_framework as filters
from .filters import *
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Max


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
#TODO 2:
      def create:
        Tambien debe crear un Staff de tipo manager asociado al owner
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
    #description = serializers.ReadOnlyField(source='describe')
    class Meta:
        model = Ref_Staff_Rol
        fields = ("id", "staff_role_code")# ,"description")

class StaffSerializer(serializers.ModelSerializer):
    staff_role_code = Ref_Staff_RolSerializer()

    class Meta:
        model = Staff
        fields = "__all__"

    def create(self, validated_data):
        
        rol_data = validated_data.pop('staff_role_code')
        rol_choice = rol_data['staff_role_code']
        rol = Ref_Staff_Rol.objects.all().filter(staff_role_code=rol_choice)
        
        staff = Staff.objects.filter(user=self.context['request'].user)
        rest = staff[0].restaurant
        restaurant = validated_data.pop('restaurant')
        
        new_staff = Staff.objects.create(staff_role_code=rol[0],restaurant = rest, **validated_data)
        return new_staff
    
    def update(self, instance, validated_data):
        
        staff = Staff.objects.filter(user=self.context['request'].user)
        rest = staff[0].restaurant
        
        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.is_active = validated_data.pop('is_active')
        instance.staff_role_code = validated_data.pop('staff_role_code')
        instance.hourly_rate = validated_data.pop('hourly_rate')
        instance.notes = validated_data.pop('notes')
        instance.restaurant = rest
       
        instance.save()
        return instance
    
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"

    def create(self, validated_data):
        """
        Crea una mesa con el numero consecutivo al existente
        Nota: ignora el parametro 'number' que le pasamos por la peticion
        Nota2: Lleva un contador para cada tipo de mesa
        """

        #Debug:
        print(self.context)
        print(validated_data)

        number = validated_data.pop('number')
        #Filtramos las mesas por restaurante y por tipo de mesa
        tables = Table.objects.all()
        staff = Staff.objects.filter(user=self.context['request'].user)
        rest = staff[0].restaurant
        restaurant = validated_data.pop('restaurant')
        ttab = validated_data['type_table']
        tables = tables.filter(restaurant=rest).filter(type_table=ttab)

        print(tables)
        if len(tables)==0:
            next_number = 1  #Caso de la primera mesa de ese tipo
        else:
            #Buscamos la mesa de mayor numero:
            next_number = tables.aggregate(Max('number'))['number__max'] + 1
        #Creamos la mesa con el siguiente numero
        new_table = Table.objects.create(number=next_number,restaurant = rest, **validated_data)
        return new_table


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = "__all__"

class Product_ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Class
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

""""
##
#  viewsets:
##
"""


class MesureUnityViewSet(viewsets.ModelViewSet):
    queryset = Mesure_Unity.objects.all()
    serializer_class = MesureUnitySerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    #TODO test get_queryset
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        """
        Se filtra por primary key del restaurante asociado al staff asociado
        al user de django que hace la peticion
        """
        staff = Staff.objects.filter(user=self.request.user)
        return self.queryset.filter(pk=staff[0].restaurant.pk)


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

    #TODO FIX get_queryset
    def get_queryset(self):
        owner_local = Owner.objects.filter(user=self.request.user)
      
        #TODO comprobar si len(owner_local) es cero y actuar en consecuenca
        #Esto significaria que el usuario que hace la peticion no es un propietario...
        if(len(owner_local)>0):
            restaurant_local = Restaurant.objects.filter(owner=owner_local[0])
            return self.queryset.filter(restaurant=restaurant_local[0])

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_class = TableFilter

    def get_queryset(self):
        #Nos quedamos solo con los objetos del usuario que lanza la peticion
        staff = Staff.objects.filter(user=self.request.user)
        print(self.request.user.username)
        return self.queryset.filter(restaurant=staff[0].restaurant).order_by('type_table')



class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class Product_ClassViewSet(viewsets.ModelViewSet):
    queryset = Product_Class.objects.all()
    serializer_class = Product_ClassSerializer
    filter_backend = filters.DjangoFilterBackend
    filter_class = Product_ClassFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter

    #TODO test get_queryset
    def get_queryset(self):
        staff = Staff.objects.filter(user=self.request.user)
        print(self.request.user.username)
        return self.queryset.filter(restaurant=staff[0].restaurant.pk)


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
router.register(r'families', FamilyViewSet)
router.register(r'product_classes', Product_ClassViewSet)
router.register(r'products', ProductViewSet)
router.register(r'ticket_resumes', Ticket_ResumeViewSet)
router.register(r'ticket_details', Ticket_DetailViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'inventory', InventoryViewSet)
