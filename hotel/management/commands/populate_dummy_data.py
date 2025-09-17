from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hotel.models import Hotel, Menu, Cart, CartItem, Order, OrderItem
from user.models import CustomUser
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write("Creating dummy data...")

        # Create Users
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'phone_number': 701234567,  # Smaller number without country code
                'first_name': 'John',
                'last_name': 'Doe'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'phone_number': 702345678,
                'first_name': 'Jane',
                'last_name': 'Smith'
            },
            {
                'username': 'mike_wilson',
                'email': 'mike@example.com',
                'phone_number': 703456789,
                'first_name': 'Mike',
                'last_name': 'Wilson'
            },
            {
                'username': 'sarah_johnson',
                'email': 'sarah@example.com',
                'phone_number': 704567890,
                'first_name': 'Sarah',
                'last_name': 'Johnson'
            },
            {
                'username': 'alex_brown',
                'email': 'alex@example.com',
                'phone_number': 705678901,
                'first_name': 'Alex',
                'last_name': 'Brown'
            }
        ]

        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'phone_number': user_data['phone_number'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(f"Created user: {user.username}")
            created_users.append(user)

        # Create Hotels
        hotels_data = [
            {
                'name': 'The Grand Restaurant',
                'location': 'Nairobi CBD, Kenya',
                'phone': '+254701111111',
                'email': 'info@grandrestaurant.com'
            },
            {
                'name': 'Coastal Delights',
                'location': 'Mombasa, Kenya',
                'phone': '+254702222222',
                'email': 'contact@coastaldelights.com'
            },
            {
                'name': 'Mountain View Bistro',
                'location': 'Nakuru, Kenya',
                'phone': '+254703333333',
                'email': 'hello@mountainviewbistro.com'
            },
            {
                'name': 'Safari Kitchen',
                'location': 'Maasai Mara, Kenya',
                'phone': '+254704444444',
                'email': 'reservations@safarikitchen.com'
            }
        ]

        created_hotels = []
        for i, hotel_data in enumerate(hotels_data):
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults={
                    'owner': created_users[i % len(created_users)],  # Cycle through users as owners
                    'location': hotel_data['location'],
                    'phone': hotel_data['phone'],
                    'email': hotel_data['email']
                }
            )
            if created:
                self.stdout.write(f"Created hotel: {hotel.name}")
            created_hotels.append(hotel)

        # Create Menu Items
        menu_items_data = [
            # Starters
            {'title': 'Caesar Salad', 'description': 'Fresh romaine lettuce with Caesar dressing, croutons, and parmesan cheese', 'price': 450, 'category': 'Starter'},
            {'title': 'Chicken Wings', 'description': 'Spicy buffalo wings served with ranch dressing', 'price': 650, 'category': 'Starter'},
            {'title': 'Samosas', 'description': 'Crispy pastries filled with spiced vegetables or meat', 'price': 300, 'category': 'Starter'},
            {'title': 'Bruschetta', 'description': 'Grilled bread topped with tomatoes, garlic, and basil', 'price': 400, 'category': 'Starter'},
            
            # Main Courses
            {'title': 'Grilled Chicken', 'description': 'Tender grilled chicken breast with herbs and spices', 'price': 1200, 'category': 'Main Course'},
            {'title': 'Beef Steak', 'description': 'Juicy beef steak cooked to perfection', 'price': 1800, 'category': 'Main Course'},
            {'title': 'Fish Fillet', 'description': 'Fresh fish fillet with lemon and herbs', 'price': 1400, 'category': 'Main Course'},
            {'title': 'Pasta Carbonara', 'description': 'Creamy pasta with bacon and parmesan cheese', 'price': 950, 'category': 'Main Course'},
            {'title': 'Vegetable Curry', 'description': 'Mixed vegetables in a rich curry sauce', 'price': 800, 'category': 'Main Course'},
            {'title': 'Pizza Margherita', 'description': 'Classic pizza with tomato sauce, mozzarella, and basil', 'price': 1100, 'category': 'Main Course'},
            {'title': 'Ugali with Sukuma Wiki', 'description': 'Traditional Kenyan meal with cornmeal and collard greens', 'price': 350, 'category': 'Main Course'},
            {'title': 'Nyama Choma', 'description': 'Grilled meat Kenyan style', 'price': 1500, 'category': 'Main Course'},
            
            # Desserts
            {'title': 'Chocolate Cake', 'description': 'Rich chocolate cake with chocolate frosting', 'price': 500, 'category': 'Dessert'},
            {'title': 'Ice Cream', 'description': 'Vanilla ice cream with chocolate sauce', 'price': 300, 'category': 'Dessert'},
            {'title': 'Tiramisu', 'description': 'Italian coffee-flavored dessert', 'price': 600, 'category': 'Dessert'},
            {'title': 'Fruit Salad', 'description': 'Fresh seasonal fruits', 'price': 400, 'category': 'Dessert'},
            
            # Beverages
            {'title': 'Coffee', 'description': 'Freshly brewed coffee', 'price': 200, 'category': 'Beverage'},
            {'title': 'Coca Cola', 'description': 'Cold Coca Cola 300ml', 'price': 100, 'category': 'Beverage'},
            {'title': 'Fresh Orange Juice', 'description': 'Freshly squeezed orange juice', 'price': 250, 'category': 'Beverage'},
            {'title': 'Tusker Beer', 'description': 'Kenyan lager beer', 'price': 300, 'category': 'Beverage'},
            {'title': 'Water', 'description': 'Bottled water 500ml', 'price': 80, 'category': 'Beverage'}
        ]

        # Available menu images in the media/menu folder
        available_images = [
            'menu/300ml_cocacola.jpg',
            'menu/beans2.jpg',
            'menu/chapati.jpg',
            'menu/coffee.jpg',
            'menu/full_chicken.jpg',
            'menu/greengrams.jpg',
            'menu/rice_beans.jpg'
        ]

        created_menus = []
        for hotel in created_hotels:
            # Each hotel gets a selection of menu items
            for menu_data in random.sample(menu_items_data, k=random.randint(10, 15)):
                menu, created = Menu.objects.get_or_create(
                    hotel=hotel,
                    title=menu_data['title'],
                    defaults={
                        'description': menu_data['description'],
                        'menu_image': random.choice(available_images),
                        'price': menu_data['price'],
                        'category': menu_data['category'],
                        'availability': random.choice([True, True, True, False])  # Mostly available
                    }
                )
                if created:
                    created_menus.append(menu)

        self.stdout.write(f"Created {len(created_menus)} menu items")

        # Create some Carts and Cart Items
        for user in created_users[:3]:  # First 3 users get carts
            cart, created = Cart.objects.get_or_create(user=user)
            if created:
                # Add random items to cart
                available_menus = list(Menu.objects.filter(availability=True))
                for _ in range(random.randint(1, 4)):
                    menu_item = random.choice(available_menus)
                    CartItem.objects.get_or_create(
                        cart=cart,
                        menu_item=menu_item,
                        defaults={'quantity': random.randint(1, 3)}
                    )
                self.stdout.write(f"Created cart for user: {user.username}")

        # Create some Orders
        order_statuses = ['Packing', 'In-transit', 'Delivered', 'Cancelled']
        for user in created_users:
            # Each user gets 1-3 orders
            for _ in range(random.randint(1, 3)):
                hotel = random.choice(created_hotels)
                order = Order.objects.create(
                    user=user,
                    hotel=hotel,
                    cost=random.randint(500, 3000),
                    status=random.choice(order_statuses)
                )
                
                # Add order items
                hotel_menus = list(Menu.objects.filter(hotel=hotel))
                for _ in range(random.randint(1, 4)):
                    menu_item = random.choice(hotel_menus)
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=Decimal(menu_item.price)
                    )

        total_orders = Order.objects.count()
        self.stdout.write(f"Created {total_orders} orders")

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDummy data created successfully!\n'
                f'Users: {len(created_users)}\n'
                f'Hotels: {len(created_hotels)}\n'
                f'Menu Items: {len(created_menus)}\n'
                f'Orders: {total_orders}\n'
                f'Carts: {Cart.objects.count()}'
            )
        )
