import requests
import openpyxl
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Order
from .serializers import ProductSerializer
from .forms import ProductForm

# --- EXISTING INVENTORY CRUD VIEWS ---

def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query).order_by('name')
    else:
        products = Product.objects.all().order_by('name')
    context = {'products': products, 'query': query}
    return render(request, 'inventory/product_list.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'product': product, 'is_update': True})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


# --- EXISTING CHECKOUT LOGIC ---

def product_buy(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Grab the name from the checkout form
        card_holder = request.POST.get('card_holder')
        
        if product.stock > 0:
            # 1. Decrease the stock
            product.stock -= 1
            product.save()
            
            # 2. CREATE THE ORDER RECORD
            Order.objects.create(
                product=product,
                card_holder=card_holder,
                price_paid=product.sale_price
            )
            
            return render(request, 'inventory/checkout_success.html', {'product': product})
            
    return render(request, 'inventory/checkout.html', {'product': product})


# --- NEW EXTRA CREDIT FEATURE: BUSINESS ANALYTICS DASHBOARD ---

@login_required
def analytics_dashboard(request):
    # Calculate global overview summary statistics from all order records
    total_sales_count = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('price_paid'))['total'] or 0
    
    # Column Chart Preparation: Total revenue generated grouped by each Game Title
    game_sales = Order.objects.values('product__name').annotate(
        total_revenue=Sum('price_paid'),
        units_sold=Count('id')
    ).order_by('-total_revenue')

    # Pie Chart Preparation: Share of transactional item units broken down per Genre
    genre_sales = Order.objects.values('product__category__name').annotate(
        units_sold=Count('id')
    ).order_by('-units_sold')

    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'game_sales': game_sales,
        'genre_sales': genre_sales,
    }
    return render(request, 'inventory/analytics.html', context)


# --- NEW EXTRA CREDIT FEATURE: DYNAMIC EXCEL REPORT EXPORTER ---

@login_required
def export_sales_excel(request):
    # Initialize a new openpyxl workspace layout
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales & Orders Ledger"

    # Insert explicit grid headers matching database schema variables
    headers = ['Order ID', 'Game Title', 'Genre (Category)', 'Buyer Name', 'Revenue Captured']
    ws.append(headers)

    # Stream all matching relational database records down ordered sequentially
    orders = Order.objects.all().order_by('-id')

    for order in orders:
        ws.append([
            order.id,
            order.product.name if order.product else "Deleted Product",
            order.product.category.name if (order.product and order.product.category) else "Uncategorized",
            order.card_holder if order.card_holder else "Anonymous Buyer",
            float(order.price_paid) if order.price_paid else 0.0
        ])

    # Construct clean application browser attachments directly on the runtime stream
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Nexus_Game_Store_Sales_Report.xlsx"'
    
    wb.save(response)
    return response


# --- EXISTING THIRD-PARTY INTEGRATIONS & API VIEWS ---

def trending_games(request):

    trending_products = Product.objects.annotate(
        copies_sold=Count('order')
    ).order_by('-copies_sold')[:9]
    
    return render(request, 'inventory/trending_games.html', {'trending_games': trending_products})

@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

def custom_logout(request):
    logout(request)
    return redirect('product_list')