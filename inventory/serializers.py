from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Only these specific fields will be translated into JSON
        fields = ['id', 'name', 'category', 'stock', 'sale_price']