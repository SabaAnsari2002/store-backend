from django.contrib import admin
from .models import Store, StoreProduct

class StoreProductInline(admin.TabularInline):
    model = StoreProduct
    extra = 1
    fields = ('product', 'price', 'stock', 'delivery_time')
    raw_id_fields = ('product',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'owner__username')
    inlines = [StoreProductInline]
    

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('store', 'product', 'price', 'stock', 'delivery_time')
    list_filter = ('store', 'product')
    search_fields = ('store__name', 'product__name')
    raw_id_fields = ('store', 'product')