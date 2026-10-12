from django.contrib import admin
from .models import Product, Brand, Size, PosterImage

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register the new Size category
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'display_sizes', 'created_at')
    list_filter = ('brand', 'sizes')
    search_fields = ('name', 'brand__name')
    
    # Creates a premium dual-listbox in the admin panel for easy multiple selection
    filter_horizontal = ('sizes',)

    # Custom method to display multiple sizes in the admin list view
    def display_sizes(self, obj):
        return ", ".join([size.abbreviation for size in obj.sizes.all()])
    display_sizes.short_description = 'Available Sizes'

@admin.register(PosterImage)
class PosterImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')