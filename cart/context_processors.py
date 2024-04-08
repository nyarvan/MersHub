from .cart import Cart


def cart(request):
    """
    Django context processor for accessing the shopping cart object
    from templates.

    Args:
        request (HttpRequest): The HttpRequest object representing
    the current request.

    Returns:
        dict: A dictionary with the shopping cart object accessible in
    templates.

    Example:
        In a Django template, you can use the 'cart' variable to access
    the cart object:
        ```
        {% if cart %}
            <p>There are {{ cart|length }} item(s) in the cart</p>
        {% endif %}
        ```

    """
    return {'cart': Cart(request)}
