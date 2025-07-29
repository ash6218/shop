from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponForm
from .models import Order, OrderItem, Coupon
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.conf import settings
import requests, json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import datetime


class CartView(View,):
    def get(self, request, order_id=None):
        cart = Cart(request) # we should use __iter__ method in cart.py so we can send an iterable value to cart.html
        return render(request, 'orders/cart.html', {'cart':cart})
    
class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product=product, quantity=form.cleaned_data['quantity'])
        return redirect('orders:cart')
    
class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')
    
class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order.html'
    form_class = CouponForm
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order':order, 'form':self.form_class})
    
    def post(self, request, order_id):
        form = self.form_class(request.POST)
        now = datetime.now()
        order = get_object_or_404(Order, id=order_id)
        if form.is_valid():
            coupon = Coupon.objects.filter(code__exact=form.cleaned_data['code'], valid_from__lte=now, valid_to__gte=now, active=True).first()
            if coupon:
                order.discount = coupon.discount
                messages.success(request, 'coupon has been activated','success')
                return render(request, self.template_name, {'order':order})
            else:
                messages.error(request, 'this coupon is not valid','danger')
                return render(request, self.template_name, {'order':order, 'form':form})
        return render(request, self.template_name, {'order':order, 'form':form})
            
                
    
class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user = request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # cart.remove(item['product']) or :
        cart.clear()
        return redirect('orders:order_detail', order.id)

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {'order_id':order.id}
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {
            'content-type': 'application/json',
            'content-length': str(len(data))
        }
        # in Production mode, dont use HttpResponse, create a nice clean html page for it  
        # and show messages with from django.contrib import messages
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    pay_url = ZP_API_STARTPAY + str(response_data['Authority'])
                    return HttpResponseRedirect(pay_url)
                else:
                    return JsonResponse(f"خطای زرین‌پال: {response_data['Status']}")
            else:
                return HttpResponse("خطا در برقراری ارتباط با زرین‌پال")

        except requests.exceptions.Timeout:
            return HttpResponse("خطا: ارتباط با زرین‌پال زمان‌بر شد")
        except requests.exceptions.ConnectionError:
            return HttpResponse("خطا: اتصال به زرین‌پال برقرار نشد")
    
class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=order_id)
        # old method: should be checked after having legit Pay portal
        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')
        if t_status == 'OK':
            req_headers = {'accept': 'application/json', 'content-type': 'application/json' }
            req_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority": t_authority,
            }
            req = request.post(url=ZP_API_VERIFY, data=json.dump(req_data), headers=req_headers)
            if len(req,json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                    order.paid = True # important to verify the successfull transaction for our website!
                    order.save()
                    # also, we should create a model and save all reference ids (RefID) 
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['data']['message']
                return HttpResponse(f'Error code: {e_code}, Error message: {e_message}')
        else:
            return HttpResponse('Transaction failed or canceled by user')
        
        # new method: should be checked after having legit Pay portal
        """data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
                order.paid = True # important to verify the successfull transaction for our website!
                order.save()
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response"""

class UnpiadOrderView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        orders = user.orders.filter(user=user, paid=False)
        return render(request, 'orders/unpaid_orders.html', {'orders':orders})
