import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Order
from .serializers import ProductSerializer
from .forms import ProductForm

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
            
    # This runs when they click "Buy Now" on the main page (GET request)
    return render(request, 'inventory/checkout.html', {'product': product})
def trending_games(request):
    api_key = '558d5ebb591f4e1291212737e3733126'  
    url = f'https://api.rawg.io/api/games?key={api_key}&ordering=-rating&page_size=10'
    games_data = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            games_data = data.get('results', [])
    except Exception:
        pass
    return render(request, 'inventory/trending_games.html', {'trending_games': games_data})

@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

def custom_logout(request):
    logout(request)
    return redirect('product_list')