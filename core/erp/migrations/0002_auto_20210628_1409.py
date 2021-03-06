# Generated by Django 3.0.5 on 2021-06-28 14:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='albar',
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
                'verbose_name': 'Albaran',
                'verbose_name_plural': 'Albaranes',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='detsale',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Factura', 'verbose_name_plural': 'Detalle de Facturas'},
        ),
        migrations.CreateModel(
            name='DetAlbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('albar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.albar')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Product')),
            ],
            options={
                'verbose_name': 'Detalle de Albaran',
                'verbose_name_plural': 'Detalle de Albaranes',
                'ordering': ['id'],
            },
        ),
    ]
