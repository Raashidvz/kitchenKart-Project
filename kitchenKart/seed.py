from Myapp.models import MenuItem
from django.contrib.auth.models import User

# Create demo users
if not User.objects.filter(username='manager').exists():
    User.objects.create_user(username='manager', password='kitchenmanager1234')
    print("Manager user created")

if not User.objects.filter(username='kitchen1').exists():
    User.objects.create_user(username='kitchen1', password='kitchenstaff1234')
    print("Kitchen user created")

# Create demo menu items
if not MenuItem.objects.exists():
    MenuItem.objects.create(name="Delicious Burger", price=120.00, image="menu_images/f2.png")
    MenuItem.objects.create(name="Delicious Pasta", price=100.00, image="menu_images/f4.png")
    MenuItem.objects.create(name="French Fries", price=80.00, image="menu_images/f5.png")
    MenuItem.objects.create(name="Double Cheese Burger", price=170.00, image="menu_images/f7.png")
    MenuItem.objects.create(name="Grilled Chicken Wrap", price=110.00, image="menu_images/grilled-chicken-wrap.webp")
    MenuItem.objects.create(name="Supreme Burger", price=180.00, image="menu_images/o1.jpg")
    MenuItem.objects.create(name="Noodles", price=150.00, image="menu_images/Noodles.png")
    MenuItem.objects.create(name="Shawarma Roll", price=100.00, image="menu_images/shawarma.webp")
    MenuItem.objects.create(name="Fried Chicken", price=220.00, image="menu_images/fried-chicken.webp")

    print("Sample menu items added")
