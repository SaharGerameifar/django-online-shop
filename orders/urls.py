from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart_add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('order_create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order_checkout/<int:random_order_id>/', views.OrderCheckOutView.as_view(), name='order_checkout'),
    path('apply/<int:random_order_id>/', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('order_pay/<int:random_order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('order_verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('order_paid/', views.PaidOrdersView.as_view(), name='order_paid'),
    path('order_paid_detail/<int:random_order_id>/', views.PaidOrderDetailView.as_view(), name='order_paid_detail'),
    path('export_factor/<int:random_order_id>/', views.export_to_pdf, name='export_factor')
]

