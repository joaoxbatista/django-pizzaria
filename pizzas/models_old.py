# from django.db import models

# class Ingredient(models.Model):
#     measure_types = (
#         ('L', '1 Litro'),
#         ('Klg', '1 Kilo'),
#         ('uni.', '1 Unidades'),
#         ('caix.', '1 Caixa'),
#         ('sac.', '1 Saco / 1 Pacote')
#     )

#     name = models.CharField(max_length=50, verbose_name="Nome")
#     unit_measure = models.CharField(max_length=20,choices=measure_types,verbose_name="Unidade de Medida")
#     price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço")
#     photo = models.ImageField(upload_to="ingredient_photos", null=True, blank=True, verbose_name="Imagem")
#     description = models.TextField(verbose_name="Descrição", null=True, blank=True)

#     def __str__(self):
#         return self.name

# class PizzaFlavor(models.Model):
#     pizzas_category = (
#         ('doces', 'doces'),
#         ('salagados', 'salagados'),
#     )
#     name =  models.CharField(max_length=50, verbose_name="Nome")
#     photo = models.ImageField(upload_to="pizzas_photos", null=True, blank=True, verbose_name="Imagem")
#     category = models.CharField(max_length=20,choices=pizzas_category)
#     price_p = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Preço do tamanho P")
#     price_m = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Preço do tamanho M")
#     price_g = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Preço do tamanho G")
#     ingredients = models.ManyToManyField(Ingredient, blank=True)

#     def __str__(self):
#         return self.name

# class Pizza(models.Model):
#     pizza_sizes = ( 
#         ('p', 'pequena'),
#         ('m', 'média'),
#         ('g', 'grande'),
#     )
#     size = models.CharField(max_length=20,choices=pizza_sizes, verbose_name="Tamanho")
#     flavors = models.ManyToManyField(PizzaFlavor, blank=True)

#     def total_price(self):
#         prices = []
#         for flavor in self.flavors.all():
#             if(self.size == 'p'):
#                 prices.append(flavor.price_p)
#             elif(self.size == 'm'):
#                 prices.append(flavor.price_m)
#             else:
#                 prices.append(flavor.price_g)
#         return sum(prices) / len(prices) 

#     def __str__(self):
#         result_name = ""
#         for flavor in self.flavors.all():
#             result_name += flavor.name + " / "
#         return result_name[:-3]

# class OrderItem(models.Model):
#     pizza = models.ForeignKey(Pizza, on_delete=models.PROTECT)
#     quantity = models.IntegerField(verbose_name="Quantidade")
#     def __str__(self):
#         return 'Quantidade: ' + str(self.quantity) + ' -> ' + str(self.pizza) +  ' | Tamanho ' + self.pizza.size

# class Order(models.Model):
#     order_types = (
#         ('entrega', 'entrega'),
#         ('mesa', 'mesa'),
#         ('viagem', 'viagem'),
#     )

#     created_at = models.DateTimeField(auto_now=True, verbose_name="Data de criação")
#     order_type = models.CharField(max_length=10, choices=order_types, verbose_name="Tipo do pedido", default="mesa")
#     discount = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Desconto")
#     order_items = models.ManyToManyField(OrderItem, blank=True) 
#     def __str__(self):
#         return str(self.pk) + ' -> ' + str(self.created_at)