import django_filters
from mainRest.models import *

class Product_ClassFilter(django_filters.FilterSet):
    """
    Atencion a las mayusculas en el nombre de la family
    """
    family = django_filters.CharFilter(name="recomended_family__name")

    class Meta:
        model = Product_Class
        fields = ('name','family')

class ProductFilter(django_filters.FilterSet):
    """
    Atencion a las mayusculas en el nombre de la family
    """
    family = django_filters.CharFilter(name="product__recomended_family__name")
    restaurant = django_filters.CharFilter(name="restaurant__name")

    class Meta:
        model = Product
        fields = ('name','restaurant', 'family', 'can_be_complement')
