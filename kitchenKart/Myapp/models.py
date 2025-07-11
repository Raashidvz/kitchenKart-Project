from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name


from django.db.models import Sum, F, DecimalField, ExpressionWrapper

class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('sent_to_kitchen', 'Sent to Kitchen'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
    ]

    order_number = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order and last_order.order_number.startswith("ORD"):
                try:
                    last_number = int(last_order.order_number.replace("ORD", ""))
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            self.order_number = f"ORD{new_number:03d}"

        super().save(*args, **kwargs)  # Save first to ensure ID exists

        # Calculate and update total after saving
        from .models import OrderItem  # Import here to avoid circular import
        total = OrderItem.objects.filter(order=self).aggregate(
            total_price=Sum(ExpressionWrapper(F('menu_item__price') * F('quantity'), output_field=DecimalField()))
        )['total_price'] or 0.00

        if self.total != total:
            self.total = total
            super().save(update_fields=['total'])

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.menu_item.name} (Order {self.order.order_number})"
    
    def total_price(self):
        return self.menu_item.price * self.quantity
