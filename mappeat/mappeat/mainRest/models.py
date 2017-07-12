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



"""
Principal Tables
"""

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.name + " " + self.surname

class Restaurant(models.Model):
    owner = models.ForeignKey(Owner, db_index=True)
    name =  models.CharField(max_length=40)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    province = models.CharField(max_length=90,blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Supply_Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Supply(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Supply_Category, null = True)

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
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    #staff_role_code = models.ForeignKey(Ref_Staff_Rol) #@DEPRECATED
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    is_active  = models.BooleanField(default=True)
    hourly_rate = models.FloatField(null=True, default=None, blank=True)
    notes = models.TextField(null=True, blank=True, default="")

    STAFF_ROLES = (
        ('W', 'Camarero'),
        ('K', 'Cocinero'),
        ('B', 'Barman'),
        ('M', 'Manager'),
    )
    role_code = models.CharField(max_length=1, choices=STAFF_ROLES, default = 'W')

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
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    table_id = models.ForeignKey(Table)
    staff_id = models.ForeignKey(Staff)
    date_of_meal = models.DateField(db_index=True, default=timezone.now())
    time_of_meal = models.TimeField(db_index=True, default = timezone.now().time())
    cost_of_meal = models.FloatField(default = 0)
    is_closed = models.BooleanField(default = False)

    #NO TESTEADO
    def close_ticket(self):
        self.is_closed = True
        self.save()

    def __str__(self):
        return str(self.date_of_meal) + ": " + self.restaurant.name



"""
Relaciona los tickets y los productos y representa cada linea de un ticket
cuando se añade un producto a una cuenta se crea una nueva instancia de Ticket_Detail
asociada a esa cuenta con el tipo de producto y la cantidad.
"""
class Ticket_Detail(models.Model):
    ticket = models.ForeignKey(Ticket_Resume, db_index=True)
    product = models.ForeignKey(Product)
    isComplement = models.BooleanField(default=False)
    quantity = models.IntegerField()
    price = models.FloatField(default = 0)
    time_of_meal = models.TimeField(default = timezone.now().time())

    def save(self, *args, **kwargs):
        #Actualiza el precio de la cuenta total:
        self.ticket.cost_of_meal = self.ticket.cost_of_meal + self.price
        super(Ticket_Resume, self.ticket).save()
        super(Ticket_Detail, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        #Actualiza el precio de la cuenta total:
        print("Hola, aqui borro: ", self.ticket.cost_of_meal, " - ", self.price)
        self.ticket.cost_of_meal = self.ticket.cost_of_meal - self.price
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
    quantity = models.IntegerField()
    mesure_unity = models.ForeignKey(Mesure_Unity, null=True)

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
    date = models.DateField(default=timezone.now, db_index=True)
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    supply = models.ForeignKey(Supply, null=True)

    quantity = models.IntegerField(default=0)
    avalible = models.BooleanField(default=False) #Indica si está agotado o aún queda
