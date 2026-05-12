from django.urls import path
from django.contrib.auth import views as auth_views # <-- Import auth views
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    
    path('buy/<int:pk>/', views.purchase_game, name='purchase_game'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('category/add/', views.category_create, name='category_create'),
    
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
]