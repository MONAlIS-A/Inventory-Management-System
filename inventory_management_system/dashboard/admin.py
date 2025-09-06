from django.contrib import admin
from . models import Product, Order, Profile
from django.contrib.auth.models import Group

# customise admin panel name
admin.site.site_header= 'Inventory Dashboard'

class ProductAdmin(admin.ModelAdmin):
    list_display =('name', 'category', 'quantity')
    list_filter = ['category']

#class OrderAdmin(admin.ModelAdmin):
   # list_display = ('product',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Profile)

# to remove Group frm admin panel
#admin.site.unregister(Group)