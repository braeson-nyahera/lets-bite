from django.shortcuts import render, redirect, get_object_or_404
from hotel.models import Menu, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    menus = Menu.objects.all()
    
    context= {
        'menus':menus,
    }
    return render(request, 'home/home.html', context)

def menulist(request):
    menu_list = Menu.objects.all()

    context = {
        'menus':menu_list,
    }

    return render(request,'home/menu_list.html', context)

# Get or create a cart for the user
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    cart = get_user_cart(request.user)

    # Check if item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{menu_item.title} added to cart.")
    return redirect('cart')

@login_required
def view_cart(request):
    cart = get_user_cart(request.user)

    context = {
        'cart': cart
    }
    return render(request, 'home/cart.html', context)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Quantity must be greater than zero.")
    return redirect('cart')

def order_summary(request):
    cart_ins = Cart.objects.get(user = request.user)
    # Retrieve the user's cart items
    menu_items = CartItem.objects.filter(cart=cart_ins.id)

    if not menu_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    total_cost = cart_ins.total_price

    context = {
        'menu_items':menu_items,
        'total_cost': total_cost
    }
    if request.method == 'POST':
        return redirect('checkout')
    
    return render(request,'home/order_summary.html', context)

@login_required
def checkout(request):
    cart_ins = Cart.objects.get(user = request.user)
    # Retrieve the user's cart items
    cart_items = CartItem.objects.filter(cart=cart_ins.id)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    # Create an order
    order = Order.objects.create(user=request.user, cost= cart_ins.total_price())
    
    # Add items to the order
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=item.menu_item.price
        )
    
    # Clear the cart
    cart_items.delete()

    messages.success(request, "Your order has been placed successfully!")
    return redirect('order-details', order_id=order.id)

def order_details(request,order_id):
    order = Order.objects.get(id= order_id)

    context = {
        'order':order
    }
    return render(request,'home/order-details.html', context)