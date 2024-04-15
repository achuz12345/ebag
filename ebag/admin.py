from django.contrib import admin
from .models import  CartItem, PenCategory,  Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image','category','manufacture','quantity']

admin.site.register(PenCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
