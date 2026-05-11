from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # THIS is the fixed line. We have to tell Django the URL is 'admin/'
    path('admin/', admin.site.urls), 
    
    # This connects your base URL directly to your store
    path('', include('inventory.urls')), 
]