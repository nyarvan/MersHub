from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from django.views.decorators.http import require_GET


def cart_detail(request):
    cart = Cart(request)
    best_seller = Product.objects.filter(best_seller=True).order_by('?')[:8]
    return render(request, 'cart.html', {'cart': cart, 'best_seller': best_seller})


@require_GET
def cart_add(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    if request.GET.get('count'):
        cart.add(product, int(request.GET.get('count')), False)
    else:
        cart.add(product, 1, False)
    return redirect('cart:cart_detail')


def cart_remove(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')