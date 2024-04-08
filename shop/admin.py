from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImages, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for managing Category instances.

    This class provides an interface for administrators to manage Category
    instances through the Django admin interface. It defines various
    settings and behaviors for how Category instances are displayed and
    edited in the admin interface.

    Attributes:
        - list_display (list): A list of field names to display
    in the list view of Category instances.
        - list_filter (list): A list of field names
    to use for filtering Category instances in the admin interface.
        - list_editable (list): A list of field names that can be edited
    directly in the list view of Category instances.
        - list_display_links (list): A list of field names to use as links
    in the list view of Category instances.
        - prepopulated_fields (dict): A dictionary specifying fields to
    auto-populate based on other fields in the admin interface.
    """
    list_display = ['name', 'slug', 'image', 'icon', 'subcategory']
    list_filter = ['subcategory']
    list_editable = ['slug', 'image', 'icon', 'subcategory']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name', )}


class ProductImagesAdmin(admin.TabularInline):
    """
    Admin class for managing ProductImages instances as inline in ProductAdmin.

    This class allows administrators to manage ProductImages instances inline
    within the ProductAdmin interface. It defines settings for how
    ProductImages instances are displayed and edited within the admin
    interface.

    Attributes:
        - model (class): The model class for which inline editing is being
    provided.
        - raw_id_fields (list): A list of field names for which raw IDs are
    displayed in the admin interface.
    """
    model = ProductImages
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin class for managing Product instances.

    This class provides an interface for administrators to manage Product
    instances through the Django admin interface. It defines various settings
    and behaviors for how Product instances are displayed and edited
    in the admin interface.

    Attributes:
        - list_display (list): A list of field names to display
    in the list view of Product instances.
        - list_filter (list): A list of field names to use for
    filtering Product instances in the admin interface.
        - list_editable (list): A list of field names that can be edited
    directly in the list view of Product instances.
        - list_display_links (list): A list of field names to use as links
    in the list view of Product instances.
        - search_fields (list): A list of field names to search for Product
    instances in the admin interface.
        - prepopulated_fields (dict): A dictionary specifying fields to
    auto-populate based on other fields in the admin interface.
        - fields (list): A list of field names to include in the edit form of
    Product instances.
        - inlines (list): A list of inline classes to include in the edit form
    of Product instances.
    """
    list_display = [
        'id', 'category', 'name', 'is_used', 'image',
        'price', 'is_special', 'count', 'available', 'best_seller',
        'new_in'
        ]
    list_filter = [
        'category', 'is_special', 'is_used',
        'available', 'best_seller', 'new_in'
        ]
    list_editable = [
        'name', 'price', 'is_used', 'is_special',
        'count', 'available', 'best_seller', 'new_in']
    list_display_links = ['id', ]
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name', )}
    fields = [
        'id', 'category', 'name', 'slug',
        'is_used', 'price', 'is_special', 'old_price',
        'description', 'remark', 'image', 'count',
        'used_quantity', 'available', 'best_seller', 'new_in'
        ]
    inlines = [ProductImagesAdmin]

    def view_image(self, obj):
        """
        Display a thumbnail of the product image.

        Args:
            obj: The Product instance.

        Returns:
            str: HTML code for displaying the thumbnail image.
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')

    view_image.short_description = 'Фотография'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin class for managing Contact instances.

    This class provides an interface for administrators to manage Contact
    instances through the Django admin interface. It defines various settings
    and behaviors for how Contact instances are displayed and edited
    in the admin interface.

    Attributes:
        - list_display (list): A list of field names to display
    in the list view of Contact instances.
        - list_editable (list): A list of field names that can be edited
    directly in the list view of Contact instances.
        - list_display_links (list): A list of field names to use as links
    in the list view of Contact instances.
        - search_fields (list): A list of field names to search for Contact
    instances in the admin interface.
    """
    list_display = ['surname', 'name', 'phone', 'email', 'is_processing']
    list_editable = ['is_processing']
    list_display_links = ['surname', ]
    search_fields = ['surname', 'name', 'phone', 'email']
