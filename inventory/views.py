from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Product, Sale   
from .forms import ProductForm, CategoryForm
from django.db.models import Sum, F

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


# --- FINANCIAL ANALYTICS DASHBOARD ---
@login_required
def analytics_dashboard(request):
    # 1. Calculate Total Revenue
    # We use F() to multiply quantity by price for every single sale in the database
    revenue_data = Sale.objects.annotate(
        line_total=F('quantity') * F('price_at_sale')
    ).aggregate(total_revenue=Sum('line_total'))
    total_revenue = revenue_data['total_revenue'] or 0.00

    # 2. Calculate Total Items Sold
    items_sold_data = Sale.objects.aggregate(total_sold=Sum('quantity'))
    total_sold = items_sold_data['total_sold'] or 0

    # 3. Find the Top 5 Best-Selling Games
    # We link the Product to its Sales, sum up the quantities, and sort descending
    top_games = Product.objects.annotate(
        total_sales=Sum('sales__quantity')
    ).filter(total_sales__gt=0).order_by('-total_sales')[:5]

    # 4. Count out-of-stock items for alerts
    out_of_stock_count = Product.objects.filter(stock=0).count()

    context = {
        'total_revenue': total_revenue,
        'total_sold': total_sold,
        'top_games': top_games,
        'out_of_stock': out_of_stock_count,
    }
    return render(request, 'inventory/dashboard.html', context)


