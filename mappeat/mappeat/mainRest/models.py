from django.db import models

# Create your models here.

class Icon(models.Model):
    image = models.ImageField()
    image_name = models.CharField(max_length=30)

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

class Meal(models.Model):
    table_id = models.ForeignKey(Table)
    staff_id = models.ForeignKey(Staff)
    date_of_meal = models.DateField()
    cost_of_meal = models.FloatField()
    
    
class Menu_Category(models.Model):
    menu_name = models.CharField(max_length=30)
    icon_class = models.ForeignKey(Icon, null=True)

    def __str__(self):
        return self.menu_name
    
class Menu_Item(models.Model):
    menu_ID = models.ForeignKey(Menu_Category)
    icon_item = models.ForeignKey(Icon, null=True)
    menu_item_name = models.CharField(max_length=30)
    price = models.FloatField(default = 0)

    def __str__(self):
        return self.menu_ID.menu_name + " | " + self.menu_item_name
    
class Meal_Dish(models.Model):
    menu_item_ID = models.ForeignKey(Menu_Item)
    quantity = models.IntegerField()
    
    
class Ingredient(models.Model):
    menu_item_ID = models.ForeignKey(Menu_Item)
    """    
    #FIXME put a default value for Icon:
    
    $ python3 manage.py makemigrations
    You are trying to change the nullable field 'icon_ingredient' on ingredient to non-nullable without a default; we can't do that (the database needs something to populate existing rows).
    Please select a fix:
    1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
    2) Ignore for now, and let me handle existing rows with NULL myself (e.g. because you added a RunPython or RunSQL operation to handle NULL values in a previous data migration)
    3) Quit, and let me add a default in models.py
    Select an option: 2
    Migrations for 'mainRest':
    mainRest/migrations/0007_auto_20170303_0142.py:
    - Alter field icon_ingredient on ingredient
    """
    icon_ingredient = models.ForeignKey(Icon)
    ingredient_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.ingredient_name
    
    