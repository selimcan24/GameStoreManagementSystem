import requests
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
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    # 1. ADD THIS NEW FIELD
    image_url = models.URLField(max_length=500, blank=True, null=True)

    # 2. OVERRIDE THE SAVE METHOD
    def save(self, *args, **kwargs):
        # Only fetch if we don't already have an image
        if not self.image_url:
            api_key = 'YOUR_API_KEY' # <-- PASTE YOUR RAWG API KEY HERE
            # Search RAWG for the exact name of the game
            url = f'https://api.rawg.io/api/games?search={self.name}&key={api_key}&page_size=1'
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    # If the API found a match, grab the background image URL
                    if data['results']:
                        self.image_url = data['results'][0].get('background_image')
            except Exception:
                pass # If the internet or API is down, just save the game normally without crashing
                
        # Call the original save method to actually save the data to the database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=100)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_holder} bought {self.product.name}"