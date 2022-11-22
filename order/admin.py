from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'phone', 'email', 'paid', 'created']
    list_filter = ['paid', ]
    search_fields = ['id', 'name', 'surname', 'phone', 'email']
    list_editable = ['paid', ]

    inlines = [OrderItemAdmin]
