# Generated by Django 2.2.7 on 2019-11-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0002_auto_20191114_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='endereco',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='tipo',
            field=models.TextField(choices=[('VIAGEM', 'VIAGEM'), ('MESA', 'MESA'), ('ENTREGA', 'ENTREGA')], default='MESA', max_length=10),
        ),
    ]
