from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        tmp = self.session.get(settings.CART_SESSION_ID)
        if tmp is None:
            tmp = self.session[settings.CART_SESSION_ID] = {}
        self.cart = tmp

    def add(self, product, count=1, update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': 0, 'price': str(product.price)}
        if update:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_product_total_price(self, product_id):
        return float(self.cart[product_id]['price'] * self.cart[product_id]['count'])

    def get_total_price(self):
        return sum(float(item['price']) * item['count'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for item in products:
            cart[str(item.id)]['product'] = item

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = float(item['price'] * item['count'])
            yield item

    def __len__(self):
        return sum(item['count'] for item in self.cart.values())
