import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name

    def get_products(self):
        category_products = Product.objects.filter(category=self)
        if len(category_products) != 0:
            return ", ".join([f"{p.product_name}" for p in category_products])
        else:
            return ""
    get_products.short_description = 'Продукция в категории'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related('product')


class Product(models.Model):
    """Products on warehouse"""
    product_name = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    quantity_per_pallet = models.PositiveIntegerField(default=1, verbose_name='Штук на паллете')
    barcode = models.CharField(max_length=64, blank=True, verbose_name='Штрихкод')


    class Meta:
        verbose_name = 'продукцию'
        verbose_name_plural = 'Продукция'

    def __str__(self):
        return self.product_name


class Order(models.Model):
    """Orders, outgoing from warehouse"""
    order_name = models.CharField(max_length=255, verbose_name='Название')
    order_date = models.DateTimeField(verbose_name='Дата')
    order_product = models.ManyToManyField(Product, through='OrderProduct')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.order_name

    def get_products(self):
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        return ", ".join([f"{p.product_name}" for p in self.order_product.all()])
    get_products.short_description = 'Продукция в заказе'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related('product')


class OrderProduct(models.Model):
    """Products in orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Отгрузка продукции'
        verbose_name_plural = 'Отгрузка продукции'

    def __str__(self):
        return f'{ self.product.product_name } ({ self.quantity } шт.)'

    def get_order_date(self):
        return self.order.order_date.strftime('%d/%m/%Y %H:%M')
    get_order_date.short_description = 'Дата заказа'


class Incoming(models.Model):
    """Incoming to warehouse"""
    incoming_name = models.CharField(max_length=255, verbose_name='Название')
    incoming_date = models.DateTimeField(verbose_name='Дата')
    incoming_product = models.ManyToManyField(Product, through='IncomingProduct')

    class Meta:
        verbose_name = 'приход'
        verbose_name_plural = 'Приход'

    def __str__(self):
        return self.incoming_name

    def get_products(self):
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        return ", ".join([f"{p.product_name}" for p in self.incoming_product.all()])
    get_products.short_description = 'Продукция в приходе'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related('product')

class IncomingProduct(models.Model):
    """Products in incoming"""
    incoming = models.ForeignKey(Incoming, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'приход продукции'
        verbose_name_plural = 'Приход продукции'

    def __str__(self):
        return f'{ self.product.product_name } ({ self.quantity } шт.)'

    def get_incoming_date(self):
        return self.incoming.incoming_date.strftime('%d/%m/%Y %H:%M')
    get_incoming_date.short_description = 'Дата прихода'