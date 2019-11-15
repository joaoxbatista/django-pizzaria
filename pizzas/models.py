from django.db import models
from django.db.models import F, FloatField, DecimalField, Sum, Avg
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

#Classe Mesa
class Mesa(models.Model):
    codigo = models.CharField(max_length=10, verbose_name="Código")

    def __str__(self):
        return 'Mesa ' + self.codigo
# Classe Sabor Pizza
class SaborPizza(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    preco_p = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço P")
    preco_m = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço M")
    preco_g = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço G")

    def __str__(self):
        return self.nome
# Classe Bebida
class Bebida(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    preco = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço")
    medida = models.CharField(max_length=10, verbose_name="Medida")
    volume = models.FloatField(verbose_name="Volume da Bebida")
    descricao = models.TextField(blank=True)

# Classe Pizza
class Pizza(models.Model):
    tamanhos = (
        ('PEQUENA', 'PEQUENA'),
        ('MEDIA', 'MEDIA'),
        ('GRANDE', 'GRANDE'),
    )
    sabores = models.ManyToManyField(SaborPizza, blank=True)
    tamanho = models.CharField(max_length=10, choices=tamanhos)
    preco = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço", blank=True, null=True)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        nome = ''
        for sabor in self.sabores.all():
            nome += sabor.nome + ' / '
        nome = nome[:-2] + ' (R$ ' + str(self.preco) + ')'
        return nome
        
    def get_preco(self):
        total = 0
        if(self.tamanho == 'PEQUENA'):
            total = self.sabores.all().aggregate(
                total_pizza = Avg((F('preco_p')), output_field=FloatField())
            )['total_pizza']
        elif(self.tamanho == 'MEDIA'):
            total = self.sabores.all().aggregate(
                total_pizza = Avg((F('preco_m')), output_field=FloatField())
            )['total_pizza']
        elif(self.tamanho == 'GRANDE'):
            total = self.sabores.all().aggregate(
                total_pizza = Avg((F('preco_g')), output_field=FloatField())
            )['total_pizza']
                
        self.preco = total

@receiver(m2m_changed, sender=Pizza.sabores.through)
def atualizar_preco_pizza(sender, instance,**kwargs):
    instance.get_preco()
    instance.save()


# Classe Venda
class Venda(models.Model):
    tipo_entrega = (
        ('VIAGEM', 'VIAGEM'),
        ('MESA', 'MESA'),
        ('ENTREGA', 'ENTREGA'),
    )
    total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Total", blank=True, null=True)
    desconto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Desconto")
    data = models.DateTimeField(auto_now=True, verbose_name="Data de criação")
    tipo = models.TextField(max_length=10, choices=tipo_entrega, default="MESA")
    endereco = models.TextField(blank=True, verbose_name="Endereço de Entrega")
    mesa = models.ForeignKey(Mesa, blank=True, null=True, on_delete=models.DO_NOTHING)
    nome_cliente = models.CharField(max_length=255, verbose_name="Nome do Cliente", default="Sem nome")

    def get_total(self):
        tot = self.itemvenda_set.all().aggregate(
            total_ped = Sum(F('quantidade') * F('pizza__preco'), output_field=DecimalField())
        )['total_ped']

        self.total = tot

        if tot:
            self.total = tot - self.desconto

        return self.total

@receiver(pre_save, sender=Venda)
def preco_com_desconto_pre(sender, instance,**kwargs):
    instance.total = instance.get_total()
    
@receiver(post_save, sender=Venda)
def preco_com_desconto_post(sender, instance,**kwargs):
    item = Venda.objects.get(pk=instance.id)
    total = item.get_total()
    Venda.objects.filter(pk=instance.id).update(total=total)



# Classe ItemVenda
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name="Quantidade", default=1)
    total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Subtotal", default=0.0)

    def get_total(self):
        self.total = self.pizza.preco * self.quantidade

@receiver(pre_save, sender=ItemVenda)
def atualizar_preco_pre(sender, instance,**kwargs):
    instance.venda.total = instance.venda.get_total()
    instance.get_total()

@receiver(post_save, sender=ItemVenda)
def atualizar_preco_venda(sender, instance,**kwargs):
    total = instance.venda.get_total()
    Venda.objects.filter(id=instance.venda.id).update(total=total)

@receiver(m2m_changed, sender=Venda)
def calcular_preco_venda(sender, instance,**kwargs):
    instance.get_total()
    