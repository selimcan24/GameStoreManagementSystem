from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Product, Sale   
from .forms import ProductForm, CategoryForm

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
        
    context = {'products': products, 'search_query': query}
    return render(request, 'inventory/product_list.html', context)


def purchase_game(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Check if we have stock
        if product.stock > 0:
            # 1. Deduct 1 from stock and save
            product.stock -= 1
            product.save()
            
            # 2. Record the sale in the database
            Sale.objects.create(
                product=product,
                quantity=1,
                price_at_sale=product.sale_price
            )
            
            # 3. Show a success message and send them home
            messages.success(request, f"Payment successful! You purchased {product.name}.")
            return redirect('product_list')
        else:
            messages.error(request, f"Sorry, {product.name} is completely sold out!")
            return redirect('product_list')

    # If they haven't submitted the form yet, show them the checkout screen
    context = {'product': product}
    return render(request, 'inventory/checkout.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'inventory/product_form.html', context)

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    context = {'form': form, 'product': product}
    return render(request, 'inventory/product_form.html', context)

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    context = {'product': product}
    return render(request, 'inventory/product_confirm_delete.html', context)

# --- THIS IS THE MISSING FUNCTION CAUSING THE CRASH ---
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'inventory/category_form.html', context)

