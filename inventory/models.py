from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    """Classifies games by genre (e.g., RPG, Shooter, Sports)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    """Represents a single game title in the store."""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    # Using DecimalField for money prevents rounding errors common with floats
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Stock cannot go below zero
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"

class Sale(models.Model):
    """Records a transaction when a game is sold."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Storing the price at the time of sale, in case the product's sale_price changes later
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.quantity}x {self.product.name} on {self.sale_date.strftime('%Y-%m-%d')}"
    
    @property
    def total_price(self):
        return self.quantity * self.price_at_sale