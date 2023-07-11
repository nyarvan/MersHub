from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImages, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image', 'icon', 'subcategory']
    list_filter = ['subcategory']
    list_editable = ['slug', 'image', 'icon', 'subcategory']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name', )}


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'is_used', 'image', 'price', 'is_special', 'count', 'available', 'best_seller', 'new_in']
    list_filter = ['category', 'is_special', 'is_used', 'available', 'best_seller', 'new_in']
    list_editable = ['name', 'price', 'is_used', 'is_special', 'count', 'available', 'best_seller', 'new_in']
    list_display_links = ['id', ]
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name', )}
    fields = ['id', 'category', 'name', 'slug', 'is_used', 'price', 'is_special', 'old_price', 'description', 'remark', 'image',
              'count', 'used_quantity', 'available', 'best_seller', 'new_in']
    inlines = [ProductImagesAdmin]

    def view_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')

    view_image.short_description = 'Фотография'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'phone', 'email', 'is_processing']
    list_editable = ['is_processing']
    list_display_links = ['surname', ]
    search_fields = ['surname', 'name', 'phone', 'email']
