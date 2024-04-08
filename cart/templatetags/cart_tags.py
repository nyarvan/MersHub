from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_product_total_price(context, product_id):
    """
    Template tag for retrieving the total price of a product in the cart.

    This template tag takes the product ID as input and retrieves
    the total price of the specified product in the shopping cart associated
    with the current request.

    Args:
        context (dict): The context dictionary containing template
    context variables.
        product_id (str): The ID of the product for which to retrieve
    the total price.

    Returns:
        float: The total price of the specified product in the shopping cart.

    """
    cart = context['cart']
    return cart.get_product_total_price(product_id)
