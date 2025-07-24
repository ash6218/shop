from .cart import Cart

def cart(request):
    return {'cart_cp': Cart(request)}