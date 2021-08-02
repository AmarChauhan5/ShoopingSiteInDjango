from django.contrib import admin
from . models import Product,Cart,OrderPlaced,Address
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','catagory','product_image']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id','user','street','village','district','state','pin_code','mobile']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','address','product','quantity','order_date','status']