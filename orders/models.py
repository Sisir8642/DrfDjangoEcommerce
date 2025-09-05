from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):

    STATUS=[
        ('pending', 'Pending'),
        ('confirmation', 'Confirmation'),
        ('cancelled', 'Cancelled'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE, related_name='orders' )
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order #{self.id} => {self.user.username}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(max_length=3)
    price_at_order = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

