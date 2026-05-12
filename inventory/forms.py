from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'purchase_price', 'sale_price', 'stock']
        # We add Bootstrap classes here so the form is dark-mode ready out of the box!
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'category': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }
        

# --- THIS IS THE FORM DJANGO WAS LOOKING FOR ---
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Strategy, Horror, Puzzle'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }