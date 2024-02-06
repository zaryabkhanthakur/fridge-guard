from django.contrib import admin
from .models import Order, FridgeItem, Suplier

class OrderAdmin(admin.ModelAdmin):
    list_display = "__all__"
class FridgeItemAdmin(admin.ModelAdmin):
    list_display = "__all__"

class SuplierAdmin(admin.ModelAdmin):
    list_display = "__all__"
    
admin.site.register(Order)
admin.site.register(FridgeItem)
admin.site.register(Suplier)


