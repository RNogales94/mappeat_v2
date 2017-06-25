import django_filters
from mainRest.models import Product_Class

class Product_ClassFilter(django_filters.FilterSet):
    """
    Atencion a las mayusculas en el nombre de la family
    """
    family = django_filters.CharFilter(name="recomended_family__name")

    class Meta:
        model = Product_Class
        fields = ('name','family')
