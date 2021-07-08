from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name= "store_store"),

    path('cart/', views.cart, name= 'store_cart'),
    path('checkout/', views.checkout, name= 'store_checkout'),

    path('update_item/', views.updateItem, name= "update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('<int:product_id>', views.detail, name="products_detail"),
    
    path('login/', views.loginPage, name="user_login"),
    path('register/', views.registerPage, name="user_register"),
    path('logout/', views.logoutPage, name= "user_logout")
]