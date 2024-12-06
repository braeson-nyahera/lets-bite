from django.urls import path
from .views import add_hotel, hotel_home, add_menu, MenuListView, MenuUpdateView, add_to_cart, view_cart,remove_from_cart,update_cart

urlpatterns = [
    path('add_hotel', add_hotel ,name='add-hotel'),
    path('menu_list', MenuListView.as_view() ,name='menu-list'),
    path('menu_update/<pk>', MenuUpdateView.as_view() ,name='menu-update'),
    path('add_menu', add_menu ,name='add-menu'),
    path('', hotel_home ,name='hotel-home'),
    path('cart/add/<int:menu_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', view_cart, name='cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update-cart'),
]
