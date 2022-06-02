from django.db import models
from accounts.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from utils import random_int, jalali_converter


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)
    address = models.TextField(max_length=500, blank=True)
    random_order_id = models.IntegerField(default=random_int, unique=True)
    refId = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=16, blank=True)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {str(self.random_order_id)} - {self.updated}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    def jupdated(self):
        return jalali_converter(self.updated)
    jupdated.short_description = 'order-updated'        


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{str(self.id)} - {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity   


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} - {self.discount} %'         
