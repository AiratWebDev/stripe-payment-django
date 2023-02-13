from django.db import models

RUBLE = 'rub'
DOLLAR = 'usd'

CURRENCY = [
    (RUBLE, 'Рубль'),
    (DOLLAR, 'Доллар'),
]


class Discount(models.Model):
    size = models.PositiveIntegerField(default=0, verbose_name='Скидка')

    class Meta:
        verbose_name = 'Размер скидки'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'{self.size}'


class Tax(models.Model):
    tax_size = models.PositiveIntegerField(default=10, verbose_name='Налог')

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Проценты налога'

    def __str__(self):
        return f'{self.tax_size}'


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    description = models.CharField(max_length=255, verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=3, default=RUBLE, choices=CURRENCY, verbose_name='Тип валюты')
    tax = models.ForeignKey(Tax, default=1, on_delete=models.PROTECT, blank=True,
                            verbose_name='Процент налога')
    discount = models.ForeignKey(Discount, default=2, on_delete=models.PROTECT, blank=True,
                                 verbose_name='Размер скидки')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def price_with_discount(self):
        return (self.price * (100 - self.discount.size)) / 100

    price_with_discount.short_description = 'Стоимость со скидкой'

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='pk')
    order = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='Покупка', null=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(default=RUBLE, choices=CURRENCY, max_length=3, verbose_name='Валюта')
    discount = models.ForeignKey(Discount, default=2, on_delete=models.PROTECT, blank=True, null=True,
                                 verbose_name='Размер скидки')
    tax = models.ForeignKey(Tax, default=1, on_delete=models.PROTECT, blank=True,
                            verbose_name='Процент налога')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_sum(self):
        return self.price * self.quantity

    get_sum.short_description = 'Сумма заказа'

    def discount_price(self):
        return (self.price * self.discount.size) / 100

    discount_price.short_description = 'Сумма скидки'

    def tax_sum(self):
        return (self.price * int(self.tax.tax_size)) / 100

    tax_sum.short_description = 'Размер налога в заказе'

    def __str__(self):
        return f"Заказ №{str(self.pk)} — {self.order}"
