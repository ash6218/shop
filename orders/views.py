from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm
class CartView(View):
    def get(self, request):
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