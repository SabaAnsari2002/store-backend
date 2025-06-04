from rest_framework import serializers

from sellers.models import Seller

class SellerSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['shop_name', 'phone', 'address', 'description', 
                 'price', 'stock', 'delivery_time']
    
    def get_price(self, obj):
        product_id = self.context.get('product_id')
        if product_id:
            product = obj.product_set.filter(id=product_id).first()
            return product.price if product else None
        return None
    
    def get_stock(self, obj):
        product_id = self.context.get('product_id')
        if product_id:
            product = obj.product_set.filter(id=product_id).first()
            return product.stock if product else 0
        return 0
    
    def get_delivery_time(self, obj):
        # می‌توانید این مقدار را از تنظیمات فروشنده یا مدل سفارشی دریافت کنید
        return "2-3 روز کاری"