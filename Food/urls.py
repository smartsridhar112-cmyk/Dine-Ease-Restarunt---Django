from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage, name='home'),
    path('categories/', FoodCategory, name='categories_list'),
    path('categories/<str:category_name>/', FoodCategory, name='food_category'),
    path('categories/<str:category_name>/<str:food_name>/', FoodCategory, name='food_category_detail'),

    path('allcart/',AllCart,name='all_cart'),
    path('addcart/<int:id>/',AddCart,name='add_cart'),
    path('addcart/quantity/<int:id>/<str:action>/',UpdateQuantity,name='update_quantity'),
    path('removecart/<int:id>/',RemoveCart,name='remove_cart'),

    path('allorder/',AllOrder,name='all_order'),
    path('addorder/<int:id>/',AddOrder,name='add_order'),
    path('removeorder/<int:id>/',RemoveOrder,name='remove_order'),

    path('allorder/checkout/',CheckOut,name='checkout'),
    path('allorder/payment-success/', payment_success, name='payment_success'),
    path('allorder/myorder/',MyOrder,name='my_orders'),

    path('search/',Search,name='search')

]
