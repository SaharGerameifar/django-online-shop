from products.models import Product


CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())        

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            if product.has_discount:
                self.cart[product_id] = {'quantity':0, 'price':str(product.super_price)}
            else:    
                self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
        temp = self.cart[product_id]['quantity'] + quantity
        if temp > 3:
            return False
        else:
            self.cart[product_id]['quantity'] = temp      
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()    

