from django.contrib import admin
from .models import *
from django.utils.html import format_html


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 2

class MesaAdmin(admin.ModelAdmin):
    fields = ('codigo',)

class SaborPizzaAdmin(admin.ModelAdmin):
    fields = ( 
        ('nome'),
        ('preco_p', 'preco_m', 'preco_g'),
        ('descricao')
    )
    
    list_display = ('id', 'nome', 'preco_p', 'preco_m', 'preco_g')

class PizzaAdmin(admin.ModelAdmin):
    fields = ('tamanho', 'observacoes', 'sabores', 'preco')
    readonly_fields = ('preco',)

class VendaAdmin(admin.ModelAdmin):
    fields = ('total', 'desconto', 'tipo', ('nome_cliente', 'mesa', 'endereco') , 'data')
    readonly_fields = ('total', 'data')
    list_display = ('id', 'data', 'tipo', 'mesa', 'nome_cliente', 'total', 'gerar_pdf')
    search_fields = ('data', 'nome_cliente')
    list_filter = ('tipo', 'data')
    inlines = [ItemVendaInline]
    
    def gerar_pdf(self, obj):
        return format_html('<a class="button">GERAR</a>')
    
    gerar_pdf.short_description = 'Gerar PDF'
    gerar_pdf.allow_tags = True

    def get_fields(self, request, obj=None):
        if obj != None:
            if obj.tipo == 'ENTREGA':
                return ('total', 'desconto', 'tipo', ('nome_cliente', 'endereco') , 'data')
            elif obj.tipo == 'MESA':
                return ('total', 'desconto', 'tipo', ('nome_cliente', 'mesa') , 'data')
            else:
                return ('total', 'desconto', 'tipo', ('nome_cliente') , 'data')

        return ('total', 'desconto', 'tipo', ('nome_cliente', 'mesa', 'endereco') , 'data')

admin.site.register(SaborPizza, SaborPizzaAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Mesa, MesaAdmin)
    
