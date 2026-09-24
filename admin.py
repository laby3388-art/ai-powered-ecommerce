from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem
admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=('name','category','price','stock','is_active'); list_filter=('category','is_active'); search_fields=('name','description')
class OrderItemInline(admin.TabularInline): model=OrderItem; extra=0; readonly_fields=('product','product_name','unit_price','quantity')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display=('id','user','status','total','created_at'); list_filter=('status','created_at'); inlines=[OrderItemInline]
admin.site.register(CartItem)
