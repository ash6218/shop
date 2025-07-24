from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin

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
    def get(self, request, order_id):
        # order = request.user.orders
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order':order})
    
class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user = request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # cart.remove(item['product']) or :
        cart.clear()
        return redirect('orders:order_detail', order.id)