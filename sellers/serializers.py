from rest_framework import serializers
from sellers.models import Seller

class SellerSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['shop_name', 'phone', 'address', 'description', 
                 'price', 'stock']
    
    def get_price(self, obj):
        product = self.get_related_product(obj)
        return product.price if product else None

    def get_stock(self, obj):
        product = self.get_related_product(obj)
        return product.stock if product else 0

    def get_related_product(self, obj):
        product_name = self.context.get('product_name')
        category_id = self.context.get('category_id')
        subcategory_id = self.context.get('subcategory_id')
        
        return obj.product_set.filter(
            name=product_name,
            category_id=category_id,
            subcategory_id=subcategory_id
        ).first()
