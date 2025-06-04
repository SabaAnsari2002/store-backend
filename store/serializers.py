from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'rating', 'price', 'stock', 'delivery_time']

    def get_price(self, obj):
        product_id = self.context.get('product_id')
        if product_id:
            store_product = obj.store_products.filter(product_id=product_id).first()
            return store_product.price if store_product else None
        return None

    def get_stock(self, obj):
        product_id = self.context.get('product_id')
        if product_id:
            store_product = obj.store_products.filter(product_id=product_id).first()
            return store_product.stock if store_product else 0
        return 0

    def get_delivery_time(self, obj):
        product_id = self.context.get('product_id')
        if product_id:
            store_product = obj.store_products.filter(product_id=product_id).first()
            return store_product.delivery_time if store_product else ""
        return ""