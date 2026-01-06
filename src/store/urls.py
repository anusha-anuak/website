from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('manage/products/', views.manage_products, name='manage_products'),
    path('product/edit/<slug:slug>/', views.edit_product, name='edit_product'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('orders/', views.order_history, name='order_history'),
    path('profile/', views.profile, name='profile'),
]

