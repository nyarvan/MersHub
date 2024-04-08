from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from shop.models import Product
from .cart import Cart


def cart_detail(request):
    """
    View function for rendering the shopping cart page.

    This view retrieves the current shopping cart and a list of
    best-selling products. It then renders the 'cart.html' template
    with the cart and best-seller data.

    Args:
        request (HttpRequest): The HttpRequest object representing
    the current request.

    Returns:
        HttpResponse: The HTTP response object containing
    the rendered template.

    """
    cart = Cart(request)
    best_seller = Product.objects.filter(best_seller=True).order_by('?')[:8]
    return render(
        request, 'cart.html', {'cart': cart, 'best_seller': best_seller})


@require_GET
def cart_add(request, product_slug):
    """
    View function for adding a product to the shopping cart.

    This view adds a specified product to the shopping cart.
    It retrieves the product using the provided slug from the URL parameters.
    If the product count is provided in the request parameters, it is used;
    otherwise, the default count is 1.
    After adding the product, the view redirects to the cart detail page.

    Args:
        request (HttpRequest): The HttpRequest object representing
    the current request.
        product_slug (str): The slug of the product to be added to the cart.

    Returns:
        HttpResponseRedirect: The HTTP response object redirecting to
    the cart detail page.

    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    count = int(request.GET.get('count', 1))
    cart.add(product, count, update=False)
    return redirect('cart:cart_detail')


def cart_remove(request, product_slug):
    """
    View function for removing a product from the shopping cart.

    This view removes a specified product from the shopping cart.
    It retrieves the product using the provided slug from the URL parameters.
    After removing the product, the view redirects to the cart detail page.

    Args:
        request (HttpRequest): The HttpRequest object representing
    the current request.
        product_slug (str): The slug of the product to be removed from
    the cart.

    Returns:
        HttpResponseRedirect: The HTTP response object redirecting to
    the cart detail page.

    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_clear(request):
    """
    View function for clearing the shopping cart.

    This view clears all products from the shopping cart.
    After clearing the cart, the view redirects to the cart detail page.

    Args:
        request (HttpRequest): The HttpRequest object representing
    the current request.

    Returns:
        HttpResponseRedirect: The HTTP response object redirecting to
    the cart detail page.

    """
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
