from django import template
from ..models import Category, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(subcategory=None).order_by('-name')


@register.simple_tag()
def get_subcategories(category_id):
    return Category.objects.filter(subcategory=category_id)


@register.simple_tag()
def get_best_seller():
    return Product.objects.filter(best_seller=True).order_by('?')[:3]


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
