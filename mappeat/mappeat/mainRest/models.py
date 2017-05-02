from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
import datetime
 
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
    
class IVA(models.Model):
    name = models.CharField(max_length=10) #Example: 'General'
    tax = models.FloatField(default=0) #0.21 = 21%
    

"""
Principal Tables
"""    

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    owner = models.ForeignKey(Owner, db_index=True)
    name =  models.CharField(max_length=40)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)

class Provider(models.Model):
    name = models.CharField(max_length=40)

class Supply_Category(models.Model):
    name = models.CharField(max_length=20)

class Supply(models.Model):
    name = models.CharField(max_length=40)

class Ref_Staff_Rol(models.Model):
    STAFF_ROLES = (
        ('W', 'Camarero'),
        ('K', 'Cocinero'),
        ('B', 'Barman'),
    )
    staf_role_description = models.CharField(max_length=1, choices=STAFF_ROLES)
    
    @staticmethod
    def staff_rol_to_str(choice):
        if choice == 'W':
            return "Camarero"
        elif choice == 'K':
            return "Cocinero"
        elif choice == 'B':
            return "Barman"
        else:
            return choice
        
    def __str__(self):
        return self.staff_rol_to_str(self.staf_role_description)

class Staff(models.Model):
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    staff_role_code = models.ForeignKey(Ref_Staff_Rol)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    
    def __str__(self):
        return (self.first_name + " " + self.last_name)
    
class Table(models.Model):
    TABLE_TYPES = (
        ('M', 'Mesa'),
        ('T', 'Terraza'),
        ('B', 'Barra'),
    )
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    number = models.IntegerField()
    type_table = models.CharField(max_length=1, choices=TABLE_TYPES)
    is_available = models.BooleanField() #Default = True
    
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
        return self.table_type_to_str(self.type_table) + " | " + str(self.number)

class Family(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ForeignKey(Icon, null=True)
    
#Product_Class (Producto Genérico) es una tabla que contiene productos propiamente dichos, como por ejemplo:
#"CocaCola" cada restaurante instanciará su propia version del producto, con un precio distinto (ver Product)
class Product_Class(models.Model):
    name = models.CharField(max_length=50)
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
    complement = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    price_as_complement = models.FloatField(default=0)
    
    restaurant = models.ForeignKey(Restaurant, db_index=True)
    product = models.ForeignKey(Product_Class, db_index=True)
    icon = models.ForeignKey(Icon, null=True)
    iva = models.ForeignKey(IVA, null=True)
    
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
    date_of_meal = models.DateField(db_index=True)
    cost_of_meal = models.FloatField()
    

"""
Relaciona los tickets y los productos y representa cada linea de un ticket
cuando se añade un producto a una cuenta se crea una nueva instancia de Ticket_Detail
asociada a esa cuenta con el tipo de producto y la cantidad.
"""
class Ticket_Detail(models.Model):
    ticket = models.ForeignKey(Ticket_Resume, db_index=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.FloatField()
    
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
    





    






