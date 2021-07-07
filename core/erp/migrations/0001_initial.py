# Generated by Django 3.0.5 on 2021-06-27 15:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('subname', models.CharField(blank=True, max_length=150, verbose_name='Subcategoria')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=150, verbose_name='Nombres')),
                ('surnames', models.CharField(blank=True, max_length=150, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=10, unique=True, verbose_name='Dni')),
                ('date_birthday', models.DateField(blank=True, default=datetime.datetime.now, verbose_name='Fecha de nacimiento')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección')),
                ('gender', models.CharField(choices=[('male', 'Masculino'), ('female', 'Femenino')], default='male', max_length=10, verbose_name='Sexo')),
                ('codigocliente', models.IntegerField(default=0, unique=True, verbose_name='Código Cliente')),
                ('codigopostal', models.CharField(max_length=5, verbose_name='Código Postal')),
                ('provincia', models.CharField(blank=True, max_length=50, verbose_name='Provincia')),
                ('prefijo', models.CharField(blank=True, max_length=3, verbose_name='Prefijo')),
                ('numtelefono', models.CharField(blank=True, max_length=7, verbose_name='Número de Telefono')),
                ('numcliente', models.IntegerField(default=0, unique=True, verbose_name='Número de Cliente')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('descuento', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Client')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de venta')),
                ('codigoarticulo', models.CharField(max_length=8, unique=True, verbose_name='Código de Articulo')),
                ('subgrupo', models.CharField(max_length=50, verbose_name='Subgrupo')),
                ('subgrupo2', models.CharField(blank=True, max_length=50, verbose_name='Subgrupo2')),
                ('nombreetiqueta', models.CharField(max_length=12, verbose_name='Nombre de Etiqueta')),
                ('stockminimo', models.IntegerField(default=0, verbose_name='Stock Mínimo')),
                ('codigobarras', models.CharField(blank=True, max_length=14, verbose_name='Código de Barras')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['id'],
            },
        ),
    ]
