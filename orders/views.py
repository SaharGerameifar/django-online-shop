from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartAddForm, CouponApplyForm, CheckOutForm
from django.contrib import messages
from .models import Order, OrderItem, Coupon
import datetime
import requests
import json
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from decouple import config
from django.template.loader import get_template
from xhtml2pdf import pisa


MERCHANT = config('MERCHANT')
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        context = {
            'cart': cart,
        }
        return render(request, self.template_name, context)


class CartAddView(PermissionRequiredMixin, View):
    permission_required = 'orders.add_order'

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity']) 
            return redirect('orders:cart')
        messages.error(request, 'بیشتر از 3 واحد و کمتر از 1 واحد از این محصول را نمی توان سفارش داد.', 'danger')    
        return redirect('products:product_detail', product.slug) 


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product) 
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity']) 
        cart.clear()
        return redirect('orders:order_checkout', order.random_order_id)


class OrderCheckOutView(LoginRequiredMixin, View):
    form_class = CheckOutForm
    form_coupon = CouponApplyForm
    template_name = 'orders/checkout.html'

    def get(self, request, random_order_id):
        order = get_object_or_404(Order, random_order_id=random_order_id)
        context = {
            'order': order,
            'form': self.form_class,
            'form_coupon': self.form_coupon,
        }
        return render(request, self.template_name, context)

    def post(self, request, random_order_id):
        order = get_object_or_404(Order, random_order_id=random_order_id)
        form = CheckOutForm(request.POST)
        if form.is_valid():
            order.post_code = form.cleaned_data['post_code']
            order.address = form.cleaned_data['address'] 
            order.save()
            return redirect('orders:order_pay', order.random_order_id)
        messages.error(request, 'لطفا اطلاعاتتان را به درستی ثبت کنید.', 'danger')    
        return redirect('orders:order_checkout', order.random_order_id)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, random_order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'این کد تخفیف معتبر نیست.', 'danger')
                return redirect('orders:order_checkout', random_order_id)
            order = Order.objects.get(random_order_id=random_order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_checkout', random_order_id)


class OrderPayView(LoginRequiredMixin, View):

    def get(self, request, random_order_id):
        order = Order.objects.get(random_order_id=random_order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):

    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                            "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.paid = True
                    order.refId = result.RefID
                    order.save()
                    order_items = OrderItem.objects.filter(order=order)
                    context ={
                        'order_items': order_items,
                        'refId': order.refId,
                        'order': order,
                    }
                    return render(request, 'orders/callback.html', context)
                    
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    messages.error(request, 'تراکنش ناموفق.\nStatus: '+ str(result.Status) , 'danger')    
                    return redirect('products:home')
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            messages.error(request, 'پرداخت توسط کاربر لغو شد.' , 'danger')    
            return redirect('products:home')


class PaidOrdersView(LoginRequiredMixin, View):
    template_name = 'orders/paidorders.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user, paid=True)
        context = {
            'orders': orders,
        }
        return render(request, self.template_name, context)


class PaidOrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/paid_order_detail.html'

    def get(self, request, random_order_id):
        order = get_object_or_404(Order, random_order_id=random_order_id, paid=True)
        context = {
            'order': order,
        }
        return render(request, self.template_name, context)


def export_to_pdf(request, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")        
    response["content-Disposition"]= 'attachment;filename=factor'+\
                                     str(datetime.datetime.now())+'.pdf'
    template_path = "orders/factorpdf.html"
    template = get_template(template_path) 
    order = get_object_or_404(Order, random_order_id=kwargs['random_order_id'], paid=True)
    context = {
        'order': order,
    } 
    html = template.render(context)     
    pisa.CreatePDF(html, dest=response) 
    return response                         