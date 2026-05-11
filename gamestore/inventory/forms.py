from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # We don't include 'stock' here because maybe we want a separate page for receiving shipments, 
        # but for this project, let's include everything the user needs to set up a game.
        fields = ['name', 'category', 'purchase_price', 'sale_price', 'stock']
        
        # Adding some basic Bootstrap styling to the form fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }