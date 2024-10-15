from django.contrib import admin

from .models import Printer, Check,Product

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('id','name','api_key','check_type','point_id')

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id','printer_id','type','order','status','pdf_file')
    list_filter = ('printer_id', 'type','status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','in_stock')