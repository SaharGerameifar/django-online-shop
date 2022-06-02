from django.contrib import admin
from .models import Order, OrderItem, Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_to', 'discount', 'active')
    search_fields = ('valid_to', 'discount')    
    list_filter = ('active',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('random_order_id', 'user', 'updated', 'paid')
    list_filter = ('paid',)
    search_fields = ('random_order_id', 'refId', 'user') 
    inlines = (OrderItemInline,)    