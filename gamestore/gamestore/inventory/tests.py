from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class InventoryTests(TestCase):
    
    def setUp(self):
        # This runs before every test to set up some dummy data
        self.category = Category.objects.create(name="RPG")
        self.product = Product.objects.create(
            name="The Witcher 3",
            category=self.category,
            purchase_price=20.00,
            sale_price=59.99,
            stock=10
        )

    # 1. MODEL TEST
    def test_product_creation(self):
        """Test that a product is created correctly in the database"""
        # Fetch the game we just made in setUp
        game = Product.objects.get(name="The Witcher 3")
        
        # Check if the data matches
        self.assertEqual(game.stock, 10)
        self.assertEqual(game.category.name, "RPG")
        # Check if our __str__ method works
        self.assertEqual(str(game), "The Witcher 3 (Stock: 10)")

    # 2. VIEW TEST
    def test_homepage_loads_correctly(self):
        """Test that the main product list page loads without errors"""
        # Simulate a user going to the homepage
        response = self.client.get(reverse('product_list'))
        
        # 200 is the standard HTTP status code for "OK"
        self.assertEqual(response.status_code, 200)
        
        # Check if the game we created shows up in the HTML
        self.assertContains(response, "The Witcher 3")