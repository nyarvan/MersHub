from django import template
from ..models import Category, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    """
    Retrieve top-level categories.

    Returns:
        QuerySet: A queryset containing top-level categories ordered by name.

    """
    return Category.objects.filter(subcategory=None).order_by('-name')


@register.simple_tag()
def get_subcategories(category_id):
    """
    Retrieve subcategories for a given category.

    Args:
        category_id (int): The ID of the parent category.

    Returns:
        QuerySet: A queryset containing subcategories for
    the specified category.

    """
    return Category.objects.filter(subcategory=category_id)


@register.simple_tag()
def get_best_seller():
    """
    Retrieve best-selling products.

    Returns:
        QuerySet: A queryset containing best-selling products
    ordered randomly, limited to 3 items.

    """
    return Product.objects.filter(best_seller=True).order_by('?')[:3]


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Replace or add query parameters in the current URL.

    Args:
        context (dict): The context dictionary containing the request object.
        **kwargs: Key-value pairs representing query parameters to
    replace or add.

    Returns:
        str: The modified URL with updated query parameters.

    """
    # Copy the current query parameters
    d = context['request'].GET.copy()
    # Update the query parameters with the provided values
    for k, v in kwargs.items():
        d[k] = v
    # Remove query parameters with empty values
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    # Encode the updated query parameters and return the modified URL
    return d.urlencode()
