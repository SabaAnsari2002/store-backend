from rest_framework import serializers
from .models import Seller

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['shop_name', 'phone', 'address', 'description']
