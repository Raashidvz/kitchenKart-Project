from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *


def signout(request):
    logout(request)
    return redirect('login')

def home(request):
    context={}
    context['foods']= MenuItem.objects.all()
    return render(request, 'index.html', context)

def sign_in(request):
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('pswd')
            user = authenticate(username=username, password=password)
            
            if user.username == "manager":
                login(request, user)
                return redirect('home')
            elif user.username == "kitchen1":
                login(request, user)
                return redirect('list_orders')
            else:
                messages.error(request, "Invalid username or password.")

    return render(request,'login_layout.html')


def place_order(request):
    if request.method == "POST":
        # Create a new order
        order = Order.objects.create()

        for key in request.POST: # Loop over each form field name submitted in the POST request
            if key.startswith("quantity_"):
                item_id = key.replace("quantity_", "")
                try:
                    quantity = int(request.POST[key])
                    if quantity > 0:
                        menu_item = MenuItem.objects.get(id=item_id)
                        OrderItem.objects.create(
                            order=order,
                            menu_item=menu_item,
                            quantity=quantity

                        )
                except (ValueError, MenuItem.DoesNotExist):
                    continue  # Ignore invalid input

        # return redirect('order_success', order_number=order.order_number)
        return redirect('home')

    return redirect('home')

# def list_orders(request):
#     context={}
#     context['order_items']= OrderItem.objects.select_related('order', 'menu_item').order_by('-order__created_at')
    
#     return render(request, 'orders.html', context)

from django.shortcuts import render
from itertools import groupby

def list_orders(request):
    # Fetch items ordered by newest first (-created_at), then by order_number
    order_items = OrderItem.objects.select_related('order', 'menu_item') \
                                  .order_by('-order__created_at', 'order__order_number')
    
    # Group by order_number (while maintaining the newest-first order)
    grouped_items = []
    current_group = []
    
    for item in order_items:
        if not current_group or item.order.order_number == current_group[0].order.order_number:
            current_group.append(item)
        else:
            # Add the group to the list (with is_first_in_group flag)
            for i, grouped_item in enumerate(current_group):
                grouped_items.append({
                    'item': grouped_item,
                    'is_first_in_group': i == 0,
                    'order': grouped_item.order,
                })
            current_group = [item]  # Start new group
    
    # Add the last group
    for i, grouped_item in enumerate(current_group):
        grouped_items.append({
            'item': grouped_item,
            'is_first_in_group': i == 0,
            'order': grouped_item.order,
        })
    
    context = {
        'grouped_items': grouped_items,
    }
    
    return render(request, 'orders.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        # Cycle through statuses or toggle to 'completed'
        if order.status != 'completed':
            order.status = 'completed'
            order.save()
    return redirect('list_orders')