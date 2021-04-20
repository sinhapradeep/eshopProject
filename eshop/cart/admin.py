from django.contrib import admin

# Register your models here.
from .models.product import Product
from .models.category import Category
from .models.order import Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCategory(admin.ModelAdmin):
        list_display = ['name']

class AdminOrder(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price' , 'address' , 'phone' , 'date']

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Order, AdminOrder)