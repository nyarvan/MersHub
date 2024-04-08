from django.conf import settings
from shop.models import Product


class Cart:
    """
    Class representing a shopping cart.

    This class handles the operations related to a shopping cart,
    such as adding, removing, and calculating total prices.

    Attributes:
        session (dict): The session object to store cart data.
        cart (dict): The dictionary representing the cart data.

    """

    def __init__(self, request):
        """
        Initializes the Cart object.

        Args:
            request: The HTTP request object.

        """

        self.session = request.session
        tmp = self.session.get(settings.CART_SESSION_ID)
        if tmp is None:
            tmp = self.session[settings.CART_SESSION_ID] = {}
        self.cart = tmp

    def add(self, product, count=1, update=False):
        """
        Adds a product to the cart.

        Args:
            product (Product): The product object to be added.
            count (int): The quantity of the product to be added.
        Defaults to 1.
            update (bool): Whether to update the quantity if the product is
        already in the cart. Defaults to False.

        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': 0, 'price': str(product.price)}
        if update:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        """Saves the cart data to the session."""
        self.session.modified = True

    def remove(self, product):
        """
        Removes a product from the cart.

        Args:
            product (Product): The product object to be removed.

        """

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Clears the cart."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_product_total_price(self, product_id):
        """
        Calculates the total price of a specific product in the cart.

        Args:
            product_id (str): The ID of the product.

        Returns:
            float: The total price of the product.

        """

        return float(
            self.cart[product_id]['price'] * self.cart[product_id]['count'])

    def get_total_price(self):
        """
        Calculates the total price of all products in the cart.

        Returns:
            float: The total price of all products in the cart.

        """

        return sum(
            float(item['price']) *
            item['count'] for item in self.cart.values())

    def __iter__(self):
        """Iterates over the items in the cart."""
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
        """
        Calculates the total number of products in the cart.

        Returns:
            int: The total number of products in the cart.

        """
        return sum(item['count'] for item in self.cart.values())
