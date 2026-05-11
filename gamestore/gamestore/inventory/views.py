from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Import our custom models and forms
from .models import Product
from .forms import ProductForm


# ---------------------------------------------------------
# PUBLIC VIEW: Anyone can view and search the store
# ---------------------------------------------------------
def product_list(request):
    # Get the search query from the URL (e.g., ?q=witcher)
    query = request.GET.get('q')
    
    if query:
        # __icontains makes it case-insensitive (finds "Witcher" even if you type "witcher")
        # .order_by('-created_at') shows the newest games first
        products = Product.objects.filter(name__icontains=query).order_by('-created_at')
    else:
        # If no search query, just show everything
        products = Product.objects.all().order_by('-created_at')
        
    # We pass the query back to the template so we can keep it in the search box
    context = {'products': products, 'search_query': query}
    return render(request, 'inventory/product_list.html', context)


# ---------------------------------------------------------
# PROTECTED VIEWS: Only logged-in users can access these
# ---------------------------------------------------------
@login_required
def product_create(request):
    if request.method == 'POST':
        # If the user clicked "Submit", save the data
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list') # Send them back to the home page
    else:
        # If they just opened the page, show a blank form
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'inventory/product_form.html', context)


@login_required
def product_update(request, pk):
    # Fetch the specific game, or show a 404 error if it doesn't exist
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # instance=product tells Django to OVERWRITE the existing game, not make a new one
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        # Pre-fill the form with the game's current data
        form = ProductForm(instance=product)
        
    context = {'form': form, 'product': product}
    return render(request, 'inventory/product_form.html', context)


@login_required
def product_delete(request, pk):
    # Fetch the specific game, or show a 404 error if it doesn't exist
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # If the user confirms on the POST request, delete the game
        product.delete()
        return redirect('product_list')
        
    # If it is just a GET request, show the "Are you sure?" confirmation page
    context = {'product': product}
    return render(request, 'inventory/product_confirm_delete.html', context)