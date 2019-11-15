import django_tables2 as tables
from .models import PizzaFlavor, Ingredient

class PizzaFlavorTable(tables.Table):
    class Meta:
        model = PizzaFlavor
        template_name = "django_tables2/bootstrap.html"
        fields =  ('name', 'category', 'price_p', 'price_m', 'price_g', 'ingredients')

class IngredientTable(tables.Table):
    class Meta:
        model = Ingredient
        template_name = "django_tables2/bootstrap.html"
        fields = ('name', 'unit_measure', 'price', 'photo', 'description')