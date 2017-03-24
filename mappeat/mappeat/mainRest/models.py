from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

"""
Secondary Tables
"""
class Icon(models.Model):
    image = models.ImageField()
    image_name = models.CharField(max_length=30)

    
    
class Mesure_Unity(models.Model):
    name = models.CharField(max_length=15)  #kilogramos
    simbol = models.CharField(max_length=3) #kg

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

class Restaurant(models.Model):
    owner = models.ForeignKey(Owner)
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

class Menu_Category(models.Model):
    menu_name = models.CharField(max_length=30)
    icon_class = models.ForeignKey(Icon, null=True)

    def __str__(self):
        return self.menu_name
class Product(models.Model):
    menu_ID = models.ForeignKey(Menu_Category)
    icon_item = models.ForeignKey(Icon, null=True)
    product_name = models.CharField(max_length=30)
    price = models.FloatField(default = 0)

    def __str__(self):
        return self.menu_ID.menu_name + " | " + self.product_name
    
       
class Ticket_Resume(models.Model):
    table_id = models.ForeignKey(Table)
    staff_id = models.ForeignKey(Staff)
    date_of_meal = models.DateField()
    cost_of_meal = models.FloatField()
    
    
"""
Relations Tables:
"""

"""
Relaciona los tickets y los productos y representa cada linea de un ticket
cuando se añade un producto a una cuenta se crea una nueva instancia de Ticket_Detail
asociada a esa cuenta con el tipo de producto y la cantidad.
"""
class Ticket_Detail(models.Model):
    ticket_ID = models.ForeignKey(Ticket_Resume)
    product_ID = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.FloatField()
    

"""
Relaciona los insumos (supply) y los productos acabados (Products)
permite hacer consultas del tipo:
A) Que productos llevan XXX ingrediente?
B) Cuales son los ingredientes del producto XXX?
"""    
class Ingredient(models.Model):
    product_ID = models.ForeignKey(Product, null=True)
    supply_ID = models.ForeignKey(Supply, null=True)
    ingredient_name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    mesure_unity = models.ForeignKey(Mesure_Unity, null=True)
    
    def __str__(self):
        return self.ingredient_name

"""
Relaciona los Restaurantes con sus compras: Materias primas (supply) y sus proveedores (Providers)
permite hacer consultas del tipo a posteriori del tipo:
A) Que Proveedores venden más XXX en una region concreta?
B) Cuales son los clientes del proveedor XXX?
"""    
class Service(models.Model):
    supply_ID = models.ForeignKey(Supply)    
    provider_ID = models.ForeignKey(Provider)    
    restaurant_ID = models.ForeignKey(Restaurant)
    date = models.DateField
    cost = models.FloatField()
    
    
"""
A efectos prácticos es el modelo que representa la carta de precios de un restaurante
"""
class Inventory(models.Model):
    product_ID = models.ForeignKey(Product)
    restaurant_ID = models.ForeignKey(Restaurant)
    actual_price = models.FloatField()
    avalible = models.BooleanField() #Indica si está agotado o aún queda
    

    
    
    





    






