from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'price', 'currency', 'tax', 'discount', 'price_with_discount']
    list_editable = ['name', 'description', 'price', 'currency', 'tax', 'discount']


@admin.register(Order)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order', 'quantity', 'price', 'currency', 'get_sum', 'discount', 'discount_price', 'tax',
                    'tax_sum']
    list_editable = ['order', 'quantity', 'price', 'currency', 'discount', 'tax']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'size']
    list_editable = ['size']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tax_size']
    list_editable = ['tax_size']
