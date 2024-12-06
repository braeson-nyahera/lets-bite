from django.urls import path
from .views import home, menulist, view_cart, add_to_cart,remove_from_cart,update_cart, checkout, order_summary, order_details

urlpatterns = [
    path('', home,name='home'),
    path('menu/',menulist, name='menu'),
    path('cart/add/<int:menu_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', view_cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', order_summary, name='order-summary'),
    path('order-details/<int:order_id>', order_details, name='order-details'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update-cart'),
]
