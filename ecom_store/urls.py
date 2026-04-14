from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
    path('categories/', views.category_list, name='category_list'),
    path('account/', views.account, name='account'),
]
