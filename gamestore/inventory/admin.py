from django.contrib import admin
from .models import Category, Product, Sale

# This registers your models so they appear in the admin panel
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)