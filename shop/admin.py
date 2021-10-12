from django.contrib import admin
from .models import *
from django.contrib.auth.models import  User

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id','product_name','category','price','pub_date']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product_name','quantity','add_time']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id','user','city','state','zip']

class Ordered_ProductInline(admin.TabularInline):
    model = Ordered_Product
    extra = 1

class Ordered_AddressInline(admin.TabularInline):
    model = Ordered_Address
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','product_count','total_amount','order_date','status']
    inlines = [Ordered_AddressInline,Ordered_ProductInline]

