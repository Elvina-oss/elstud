from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'time_create', 'time_update', 'for_sale', 'price', 'seller']
    list_display_links = ['name']
    search_fields = ['name', 'content']
    list_editable = ['for_sale']
    list_filter = ['for_sale', 'time_create']
    prepopulated_fields = {"slug": ("name",), }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name',]
    prepopulated_fields = {"slug" : ("name",),}


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
