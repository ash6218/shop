from home.models import Product


CS_ID = 'cart' # CART_SESSION_ID

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CS_ID) # CS_ID (cart) is the name of the session that we already saved
        if not cart: # if the user didnt have any cart before, we should make one for them
            cart = self.session[CS_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)  # we want products that their id is in ...
        # ...product_ids (cart keys) which is a list, not a number, so we use field lookup __in
        cart = self.cart.copy() # we want to add name of product to current cart but not the main one
        for product in products:
            cart[str(product.id)]['product'] = product # or product.name , when we use product, __str__ will be called
        for item in cart.values(): # we want the values of every product so we can calculate total price
            item['total_price'] = item['quantity']*int(item['price'])
            yield item # yield is similar to return but used for iterable values
    
    def __len__(self):
        return sum(1 for item in self.cart.values())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def get_total_price(self):
        return sum(item['total_price'] for item in self.cart.values())
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CS_ID]
        self.save()