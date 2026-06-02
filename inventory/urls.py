from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('buy/<int:pk>/', views.product_buy, name='product_buy'),
    path('trending/', views.trending_games, name='trending_games'),
    path('api/products/', views.api_product_list, name='api_product_list'),
    
    # Extra credit analytics routes
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/export/', views.export_sales_excel, name='export_sales_excel'),
    
    # Reverted back to your simple custom logout redirect
    path('logout/', views.custom_logout, name='logout'),
]