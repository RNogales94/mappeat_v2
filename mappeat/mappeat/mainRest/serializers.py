"""
Serializers
"""

from rest_framework import routers, serializers, viewsets
from django_filters import rest_framework as filters
from .filters import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.db.models import Max

from django.contrib.auth.models import User

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'password') # 'email' field can be added

    def create(self, validated_data):
        manager = Staff.objects.filter(user=self.context['request'].user)[0]
        new_user = User.objects.create_user(**validated_data)
        new_user.save()
        return new_user

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_class = UserFilter
    serializer_class = UserSerializer


"""
Serializadores para los modelos de mainRest
"""
# Serializers define the API representation.
class MesureUnitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure_Unity
        fields = "__all__"

class IVASerializer(serializers.ModelSerializer):
    strTax = serializers.SerializerMethodField()

    class Meta:
        model = IVA
        fields = ("id", "name", "tax", "strTax")
    def strTax(self, obj):
        return obj.strTax()

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

"""
# @Debug
    def create(self, validated_data):
        print(validated_data)
        return super().create()
"""



"""
# @DEPRECATED
class Ref_Staff_RolSerializer(serializers.ModelSerializer):
    #description = serializers.ReadOnlyField(source='describe')
    class Meta:
        model = Ref_Staff_Rol
        fields = ("id", "staff_role_code")# ,"description")
"""

class StaffSerializer(serializers.ModelSerializer):
    #staff_role_code = Ref_Staff_RolSerializer()

    class Meta:
        model = Staff
        fields = "__all__"

    def create(self, validated_data):
        """
        Solo puede crearse personal asociado al restaurante del creador (manager)
        """
        manager = Staff.objects.filter(user=self.context['request'].user)[0]
        rest = manager.restaurant
        restaurant = validated_data.pop('restaurant')

        new_staff = Staff.objects.create(restaurant = rest, **validated_data)
        new_staff.save()
        return new_staff

    def update(self, instance, validated_data):
        """
        Puede actualizarse todo excepto el restaurante
        """
        staff = Staff.objects.filter(user=self.context['request'].user)[0]
        rest = staff.restaurant

        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.is_active = validated_data.pop('is_active')
        instance.role_code = validated_data.pop('role_code')
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

    def create(self, validated_data):
        manager = Staff.objects.filter(user=self.context['request'].user)[0]
        rest = manager.restaurant
        restaurant = validated_data.pop('restaurant')
        new_item = Product.objects.create(restaurant = rest, **validated_data)
        return new_item

class Ticket_ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Resume
        fields = "__all__"

    def get_queryset(self):
        """
        Se filtra por primary key del restaurante asociado al staff asociado
        al user de django que hace la peticion
        """
        staff = Staff.objects.filter(user=self.request.user)
        return self.queryset.filter(pk=staff[0].restaurant.pk)



class Ticket_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Detail
        fields = ('pk', 'ticket', 'product', 'product_name', 'isComplement', 'quantity',\
                    'price', 'time', 'sent_kitchen')

    def create(self, validated_data):
        print("Creando Ticket_Detail..")
        ticket = validated_data['ticket']
        print("Aquí llega")
        p = validated_data['product']
        q = validated_data['quantity']
        iC = validated_data['isComplement']

        ticket = ticket.addTicketDetail(product_id = p.pk, quantity=q, isComplement = iC )
        new_detail = ticket.getLastDetail()
        
        return new_detail


"""
TicketSerializer
Es un serializador para el modelo Ticket_Resume
que cuenta con un campo extra 'details' para ver las lineas del ticket
directamente sin tener que hacer llamadas extra.
"""
class TicketSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Ticket_Resume
        #fields = ("__all__", 'details')   <-- basicamente es eso
        fields = ('pk', 'restaurant', 'table', 'staff', 'date',\
                    'time', 'cost', 'is_closed', 'details' )

    def get_details(self, ticket_resume):
        details = Ticket_Detail.objects.filter(ticket=ticket_resume)
        serializer = Ticket_DetailSerializer(instance=details, many=True)
        return serializer.data

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

    def create(self, validated_data):
        manager = Staff.objects.filter(user=self.context['request'].user)[0]
        rest = manager.restaurant
        restaurant = validated_data.pop('restaurant')
        new_item = Inventory.objects.create(restaurant = rest, **validated_data)
        return new_item
""""
##
#  viewsets:
##
"""


class MesureUnityViewSet(viewsets.ModelViewSet):
    queryset = Mesure_Unity.objects.all()
    serializer_class = MesureUnitySerializer

class IVAViewSet(viewsets.ModelViewSet):
    queryset = IVA.objects.all()
    serializer_class = IVASerializer

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

"""
# @DEPRECATED
class Ref_Staff_RolViewSet(viewsets.ModelViewSet):
    queryset = Ref_Staff_Rol.objects.all()
    serializer_class = Ref_Staff_RolSerializer

"""
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    """
    Cambiar owner por manager para que los owners no sean necesarios
    """

    def get_queryset(self):
        staff = Staff.objects.filter(user=self.request.user)
        print(staff)
        restaurant = staff[0].restaurant
        print(restaurant)
        if staff[0].role_code=='M':
            return self.queryset.filter(restaurant=restaurant)
        else:
            return self.queryset.filter(restaurant=restaurant, user=self.request.user)


    """
    def get_queryset(self):
        staff = Staff.objects.filter(user=self.request.user)
        restaurant = staff[0].restaurant

        boss = Staff.objects.filter(restaurant=restaurant, role_code='M') #M = manager
        print(boss)
        #Comprobar si len(owner_local) es cero y actuar en consecuenca
        #Esto significaria que el usuario que hace la peticion no es un propietario...
        if(len(boss)>0):
            owner = Owner.objects.filter(user=boss[0].user)
            print(owner)
            restaurant_local = Restaurant.objects.filter(owner=owner[0])
            return self.queryset.filter(restaurant=restaurant_local[0])
    """
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
    filter_class = Ticket_ResumeFilter

    def get_queryset(self):
        """
        Se filtra por primary key del restaurante asociado al staff asociado
        al user de django que hace la peticion
        """
        staff = Staff.objects.filter(user=self.request.user)
        return self.queryset.filter(restaurant=staff[0].restaurant.pk)

class Ticket_DetailViewSet(viewsets.ModelViewSet):
    queryset = Ticket_Detail.objects.all()
    serializer_class = Ticket_DetailSerializer
    filter_class = Ticket_DetailFilter

    def get_queryset(self):
        """
        Se filtra por primary key del restaurante asociado al staff asociado
        al user de django que hace la peticion
        """
        staff = Staff.objects.filter(user=self.request.user)
        return self.queryset.filter(ticket__restaurant=staff[0].restaurant.pk)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket_Resume.objects.all()
    serializer_class = TicketSerializer
    filter_class = TicketFilter
    def get_queryset(self):
        """
        Se filtra por primary key del restaurante asociado al staff asociado
        al user de django que hace la peticion
        """
        staff = Staff.objects.filter(user=self.request.user)
        return self.queryset.filter(restaurant=staff[0].restaurant.pk)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    filter_class = IngredientFilter
    serializer_class = IngredientSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'mesureUnities', MesureUnityViewSet)
router.register(r'iva', IVAViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'suply_categories', Supply_CategoryViewSet)
router.register(r'suplies', SupplyViewSet)
#router.register(r'ref_staff_roles', Ref_Staff_RolViewSet) #@DEPRECATED
router.register(r'staff', StaffViewSet)
router.register(r'tables', TableViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'product_classes', Product_ClassViewSet)
router.register(r'products', ProductViewSet)
router.register(r'ticket_resumes', Ticket_ResumeViewSet)
router.register(r'ticket_details', Ticket_DetailViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'inventory', InventoryViewSet)
