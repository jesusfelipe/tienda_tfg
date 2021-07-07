from datetime import datetime

from djongo import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    subname = models.CharField(max_length=150, verbose_name='Subcategoria', blank=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    codigoarticulo = models.CharField(max_length=8, verbose_name='Código de Articulo', unique=True)
    subgrupo = models.CharField(max_length=50, verbose_name='Subgrupo')
    subgrupo2 = models.CharField(max_length=50, verbose_name='Subgrupo2', blank=True)
    nombreetiqueta = models.CharField(max_length=12, verbose_name='Nombre de Etiqueta')
    stockminimo = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    codigobarras = models.CharField(max_length=14, verbose_name='Código de Barras', blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp)
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos', blank=True)
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento', blank=True)
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    codigocliente = models.IntegerField(default=0, unique=True, verbose_name='Código Cliente')
    codigopostal = models.CharField(max_length=5, verbose_name='Código Postal')
    provincia = models.CharField(max_length=50,verbose_name='Provincia', blank=True)
    prefijo = models.CharField(max_length=3, verbose_name='Prefijo', blank=True)
    numtelefono = models.CharField(max_length=7, verbose_name='Número de Telefono', blank=True)
    numcliente = models.IntegerField(default=0, verbose_name='Número de Cliente', unique=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descuento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal)
        item['iva'] = format(self.iva)
        item['total'] = format(self.total)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        item['descuento'] = format(self.descuento)
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price)
        item['subtotal'] = format(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalle de Facturas'
        ordering = ['id']


class Albar(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descuento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal)
        item['iva'] = format(self.iva)
        item['total'] = format(self.total)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detalbar_set.all()]
        item['descuento'] = format(self.descuento)
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detalbar_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Albar, self).delete()

    class Meta:
        verbose_name = 'Albaran'
        verbose_name_plural = 'Albaranes'
        ordering = ['id']


class DetAlbar(models.Model):
    albar = models.ForeignKey(Albar, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['albar'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price)
        item['subtotal'] = format(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Albaran'
        verbose_name_plural = 'Detalle de Albaranes'
        ordering = ['id']
