from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_product_total_price(context, product_id):
    cart = context['cart']
    return cart.get_product_total_price(product_id)
