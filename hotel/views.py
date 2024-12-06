from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HotelForm, MenuForm
from django.utils.html import strip_tags
from .models import Menu,Hotel,Cart, CartItem
from django.views.generic import ListView, UpdateView


# Create your views here.

def hotel_home(request):
    hotel = Hotel.objects.get(owner=request.user)
    menu = Menu.objects.filter(hotel=hotel.id)

    context = {
        'menu': menu,
    }
    return render(request,'hotel/hotel_home.html', context)

def add_hotel(request):
    form = HotelForm()
    if request.method == 'POST':
        form = HotelForm(request.POST)

        if form.is_valid():
            
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()

            messages.success(request,f"{hotel.name} has been registered successfully. Please wait for admin confirmation.")
            return redirect('home')
        else: 
            error = strip_tags(form.errors)
            messages.error(request,f"Error: {error}")
            
    
    return render(request,'hotel/add_hotel.html',{'form':form})
    
def add_menu(request):
    categories = Menu.Category.choices
    menu_form = MenuForm()

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, request.FILES)

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            hotel_ins = Hotel.objects.get(owner=request.user)
            menu.hotel = hotel_ins 
            menu.save()

            messages.success(request,f"{menu.title} has been added successfully")
            return redirect('menu-list')
        else:
            error = strip_tags(menu_form.errors)
            messages.error(request,f"Error: {error}")

    context = {
        'categories':categories
    }
    return render(request,'hotel/add_menu.html', context)

class MenuListView(ListView):
    model = Menu
    template_name = 'hotel/menu_list.html'
    context_object_name = 'menus'

    def get_queryset(self):
        hotel_id = Hotel.objects.get(owner = self.request.user)
        return Menu.objects.filter(hotel=hotel_id).order_by('-updated_at')
    
class MenuUpdateView(UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'hotel/menu_update.html'
    
    def form_valid(self, form):
        # Debug uploaded file
        menu_image = self.request.FILES.get('menu_image')
        print(f"Uploaded menu_image: {menu_image}")
        
        # Save form and handle any additional processing
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('menu-list')
    




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
