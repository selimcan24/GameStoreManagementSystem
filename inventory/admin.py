from django.contrib import admin
# MAKE SURE 'Order' IS ADDED TO THIS LINE BELOW
from .models import Product, Category, Order 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_date', 'card_holder', 'product', 'price_paid')
    list_filter = ('purchase_date', 'product')
    search_fields = ('card_holder', 'product__name')

# Your other registrations below...
admin.site.register(Category)
admin.site.register(Product)