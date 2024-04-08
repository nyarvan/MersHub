from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    """
    Inline admin class for managing order items.

    This inline admin class is used to display and manage order items within
    the order admin interface.

    Attributes:
        model (Model): The model class representing the order item.
        raw_id_fields (list): A list of fields to be displayed as raw IDs.
    """

    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for managing orders.

    This admin class is used to manage orders within
    the Django admin interface.

    Attributes:
        list_display (list): A list of fields to be displayed
    in the order list view.
        list_filter (list): A list of fields to be used as filters
    in the order list view.
        search_fields (list): A list of fields to be used as search criteria
    in the order list view.
        list_editable (list): A list of fields that can be edited directly
    in the order list view.
        inlines (list): A list of inline admin classes to be displayed within
    the order admin interface.

    """

    list_display = [
        'id', 'name', 'surname', 'phone',
        'email', 'paid', 'created']
    list_filter = ['paid', ]
    search_fields = ['id', 'name', 'surname', 'phone', 'email']
    list_editable = ['paid', ]

    inlines = [OrderItemAdmin]
