from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

"""
Secondary Tables
"""
class Icon(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Mesure_Unity(models.Model):
    name = models.CharField(max_length=15)  #kilogramos
    simbol = models.CharField(max_length=3) #kg

    def __str__(self):
        return self.name

class IVA(models.Model):
    name = models.CharField(max_length=15) #Example: 'General'
    tax = models.FloatField(default=0) #0.21 = 21%

    def __str__(self):
        return self.name

    def strTax(self):
        return str(self.tax)+"%"



"""
Principal Tables
"""

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name + " " + self.surname

class Restaurant(models.Model):
    owner = models.OneToOneField(Owner, db_index=True)
    name =  models.CharField(max_length=40)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    province = models.CharField(max_length=90,blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self):
        owner = self.owner
        owner.delete()
        super(Restaurant, self).delete()

class Provider(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

"""
La categoría de un supply (suministro) puede ser una de las siguientes:
 * Servicio  (TODO: Los servicios no aparecen listados en el inventario)
 * Articulo (TODO: Los articulos aparecen listados en el inventario)
 * Otros  (Se evitará su uso)
"""

class Supply_Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

"""
Los Supply (suministros) son las cosas que compra un cliente
"""

class Supply(models.Model):
    name = models.CharField(max_length=40)
    size = models.FloatField(null=True)
    mesure_unity = models.ForeignKey(Mesure_Unity, null=True)
    is_storable = models.BooleanField(default=True)
    category = models.ForeignKey(Supply_Category, null = True)
    barcode = models.IntegerField(null = True)

    def __str__(self):
        return self.name
"""
# @DEPRECATED
class Ref_Staff_Rol(models.Model):
    STAFF_ROLES = (
        ('W', 'Camarero'),
        ('K', 'Cocinero'),
        ('B', 'Barman'),
        ('M', 'Manager'),
    )
    staff_role_code = models.CharField(max_length=1, choices=STAFF_ROLES)

    @staticmethod
    def staff_rol_to_str(choice):
        if choice == 'W':
            return "Camarero"
        elif choice == 'K':
            return "Cocinero"
        elif choice == 'B':
            return "Barman"
        elif choice == 'M':
            return "Manager"
        else:
            return choice

    def __str__(self):
        return self.staff_rol_to_str(self.staff_role_code)

"""

class Staff(models.Model):
    user = models.OneToOneField(User, db_index=True, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, db_index=True, null=True)
    #staff_role_code = models.ForeignKey(Ref_Staff_Rol) #@DEPRECATED
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=50, default="")
    is_active  = models.BooleanField(default=True)
    hourly_rate = models.FloatField(null=True, default=None, blank=True)
    notes = models.TextField(null=True, blank=True, default="")

    STAFF_ROLES = (
        ('W', 'Camarero'),
        ('K', 'Cocinero'),
        ('B', 'Barman'),
        ('M', 'Manager'),
    )
    role_code = models.CharField(max_length=1, choices=STAFF_ROLES, default = 'M')

    """
    Mejoras a tener en cuenta:
    Añadir unos días de trabajo habituales, de forma que se le envíe un email
    al manager en el caso de que un empleado haga login fuera de su horario habitual
    (pero que sea solo una medida de control extra y en ningun caso impida hacer login
    puesto que podría ser porque se han cambiado el día dos camareros o cosas asi
    que son bastante habituales)
    """
    @staticmethod
    def role_to_str(choice):
        if choice == 'W':
            return "Camarero"
        elif choice == 'K':
            return "Cocinero"
        elif choice == 'B':
            return "Barman"
        elif choice == 'M':
            return "Manager"
        else:
            return choice

    def __str__(self):
        return (self.first_name + " " + self.last_name + " " + self.role_to_str(self.role_code))

class Table(models.Model):
    TABLE_TYPES = (
        ('M', 'Mesa'),
        ('T', 'Terraza'),
        ('B', 'Barra'),
    )
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    number = models.IntegerField()
    type_table = models.CharField(max_length=1, choices=TABLE_TYPES)
    is_available = models.BooleanField(default=True) #Default = True

    class Meta:
        unique_together = ('number', 'restaurant', 'type_table')

    @staticmethod
    def table_type_to_str(choice):
        if choice == 'M':
            return "Mesa"
        elif choice == 'T':
            return "Terraza"
        elif choice == 'B':
            return "Barra"
        else:
            return choice

    def __str__(self):
        rest = self.restaurant.name
        type_table = self.table_type_to_str(self.type_table)
        number = str(self.number)
        return type_table + " | " + number + " | " + rest

class Family(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.ForeignKey(Icon, null=True)

    def __str__(self):
        return self.name


#Product_Class (Producto Genérico) es una tabla que contiene productos propiamente dichos, como por ejemplo:
#"CocaCola" cada restaurante instanciará su propia version del producto, con un precio distinto (ver Product)
class Product_Class(models.Model):
    name = models.CharField(max_length=50, unique = True)
    icon = models.ForeignKey(Icon, null=True)
    recomended_family = models.ForeignKey(Family, null=True)

    def __str__(self):
        return self.name

"""
Product:
Es la especificación que cada restaurante toma de un producto generico (Product_Class)
Por ejemplo del Product_Class "coca cola" se pueden extraer los productos:
    - CocaCola mediana (330ml) 2.50€
    - CocaCola pequeña (127ml) 1.50€
La tabla Product puede considerarse como las "cartas" de todos los restaurantes
filtrando por el campo 'restaurant' tenemos la carta de un restaurante concreto
"""
class Product(models.Model):
    name = models.CharField(max_length=50)
    principal = models.BooleanField(default=True)
    can_be_complement = models.BooleanField(default=False)
    price_with_tax = models.FloatField(default=0)
    price_as_complement_with_tax = models.FloatField(default=0)

    restaurant = models.ForeignKey(Restaurant, db_index=True) #Se usa el db_index
    product = models.ForeignKey(Product_Class, db_index=True)
    icon = models.ForeignKey(Icon, null=True)
    iva_tax = models.ForeignKey(IVA, null=True)

    class Meta:
        unique_together = ('name', 'restaurant',)

    def __str__(self):
        return self.product.name + ": (" + self.name + ")"

"""
Product_Family:
Tabla que permite que un producto esté asociado a varias familias
product='coca cola', family='bebidas'
proudct='coca cola', family='refrescos'
"""
class Product_Family(models.Model):
    restaurant = models.ForeignKey(Restaurant, db_index=True, null=True) #Optimiza consultas (Filtro)
    family = models.ForeignKey(Family, db_index=True)
    product = models.ForeignKey(Product)


class Ticket_Resume(models.Model):
    def defaultTime():
        return timezone.now().time().replace(microsecond=0)
    def defaultDate():
        return timezone.now().date()
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    table = models.ForeignKey(Table)
    staff = models.ForeignKey(Staff)
    date = models.DateField(db_index=True, default=defaultDate)
    time = models.TimeField(db_index=True, default=defaultTime)
    cost = models.FloatField(default = 0)
    is_closed = models.BooleanField(default = False, db_index=True)

    def addTicketDetail(self, product_id, quantity=1, isComplement=False):
        #Sacamos el ultimo ticket_detail de este ticket
        details = Ticket_Detail.objects.all().filter(ticket=self)
        print(details)

        lastDetail = details.order_by('-time')[0]
        print(lastDetail)
        product_local = Product.objects.all().filter(pk=product_id)[0]
        mismoProducto = product_local == lastDetail.product
        if not len(details) == 0 and mismoProducto:
            lastDetail.quantity += quantity
            lastDetail.save()
        else:
            if not isComplement:
                price = product_local.price_with_tax
            else:
                price = product_local.price_as_complement_with_tax

            new_detail = Ticket_Detail(ticket = self,
                          product = product_local,
                          product_name = product_local.name,
                          isComplement = isComplement,
                          quantity = quantity,
                          price = price)
            new_detail.save()

    #NO TESTEADO
    def close_ticket(self):
        self.is_closed = True
        self.save()

    def __str__(self):
        return str(self.date) + ": " + self.restaurant.name



"""
Relaciona los tickets y los productos y representa cada linea de un ticket
cuando se añade un producto a una cuenta se crea una nueva instancia de Ticket_Detail
asociada a esa cuenta con el tipo de producto y la cantidad.
"""
class Ticket_Detail(models.Model):
    """
    IMPORTANTE:

    Al añadir aqui un campo no se añade automaticamente en la api
    Hay que añadirlo manualmente en serializers.py
    """
    def defaultTime():
        return timezone.now().time().replace(microsecond=0)

    ticket = models.ForeignKey(Ticket_Resume, db_index=True)
    product = models.ForeignKey(Product, null=True)
    product_name = models.CharField(max_length = 50, default="None")
    isComplement = models.BooleanField(default=False)
    quantity = models.IntegerField()
    price = models.FloatField(default = 0)
    time = models.TimeField(default=defaultTime)
    sent_kitchen = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        """
        Establece el nombre del producto la primera vez al crearse
        #esto previene cambio de nombre en los tickets al cambiar el nombre
        del producto

        Lo mismo ocurre con el precio
        """
        #Este if es True solo la primera vez para cada Ticket_Detail
        if self.product_name == "None":
            print("Entra por None")
            self.product_name = self.product.name

            if self.isComplement:
                self.price = self.product.price_as_complement_with_tax
            else:
                self.price = self.product.price_with_tax

            #Actualiza el precio de la cuenta total:
            self.ticket.cost = self.ticket.cost + self.price
            super(Ticket_Resume, self.ticket).save()

        #A partir de aqui se ejecuta cada vez que actualizamos un Ticket_Detail
        print("Ticket Detail")
        print(self.time)
        super(Ticket_Detail, self).save()
        #super(Ticket_Detail, self).save(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        #Actualiza el precio de la cuenta total:
        print("Hola, aqui borro: ", self.ticket.cost, " - ", self.price)
        self.ticket.cost = self.ticket.cost - self.price
        super(Ticket_Resume, self.ticket).save()
        super(Ticket_Detail, self).delete(*args, **kwargs)


    def __str__(self):
        return self.product.name + "  × " + str(self.quantity) +": ------  "+ str(self.price) + "€"

"""
Ingredient:
Puede verse como la receta de un producto compuesto por varios insumos (supply):

Relaciona los insumos (supply) y los productos acabados (Products)
permite hacer consultas del tipo:
A) Que productos llevan XXX ingrediente?
B) Cuales son los ingredientes del producto XXX?
"""
class Ingredient(models.Model):
    quantity = models.FloatField()
    supply = models.ForeignKey(Supply, null=True)
    product = models.ForeignKey(Product, null=True)

    def __str__(self):
        return self.product.name + " ingredients"

"""
Service:
Relaciona los Restaurantes con sus compras: Materias primas (supply) y sus proveedores (Providers)
permite hacer consultas del tipo a posteriori del tipo:
A) Que Proveedores venden más XXX en una region concreta?
B) Cuales son los clientes del proveedor XXX?
"""
class Service(models.Model):
    date = models.DateField()
    cost = models.FloatField()

    supply = models.ForeignKey(Supply)
    provider = models.ForeignKey(Provider)
    restaurant = models.ForeignKey(Restaurant)

"""
Inventory:
Representa las existencias en el almacen de un determinado suministro un determinado día
"""
class Inventory(models.Model):
    def defaultDate():
        return timezone.now().date()

    date = models.DateField(default=defaultDate, db_index=True)
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    supply = models.ForeignKey(Supply, null=True)

    quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=False) #Indica si está agotado o aún queda
