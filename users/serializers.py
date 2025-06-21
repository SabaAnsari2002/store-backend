from rest_framework import serializers

# from sellers.models import Seller

from .models import CustomUser, StoreRole, Ticket, TicketReply, Discount, Address, BankCard
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = self.user.id 
        data['username'] = self.user.username

        return data

class TicketReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_staff_reply = serializers.BooleanField(default=False)

    class Meta:
        model = TicketReply
        fields = ['id', 'user', 'message', 'is_staff_reply', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_user(self, obj):
        if not obj.user:
            return None
            
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'is_staff': obj.user.is_staff
        }



class TicketSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    replies = TicketReplySerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'subject', 'message', 'status', 'status_display',
            'priority', 'priority_display', 'category', 'category_display',
            'order_id', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        if not obj.user:
            return None
            
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'is_staff': obj.user.is_staff
        }

class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ['id', 'card_name', 'card_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
        extra_kwargs = {
    'card_number': {
        'required': True,
        'min_length': 16,
        'max_length': 16
    }
}


        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'title', 'address_line', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'password', 'new_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return value

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)

        if new_password:
            if not password:
                raise serializers.ValidationError({"password": "برای تغییر رمز عبور، رمز عبور فعلی را وارد کنید."})
            if not instance.check_password(password):
                raise serializers.ValidationError({"password": "رمز عبور فعلی نادرست است."})
            instance.set_password(new_password)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', '')
        )
        return user 
class DiscountSerializer(serializers.ModelSerializer):
    remaining_time = serializers.SerializerMethodField()
    seller_name = serializers.CharField(source='seller.user.username', read_only=True)

    class Meta:
        model = Discount
        fields = [
            'id', 
            'seller', 
            'seller_name',
            'title', 
            'code', 
            'description', 
            'percentage', 
            'is_active', 
            'for_first_purchase', 
            'created_at',
            'updated_at',
            'remaining_time'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def get_remaining_time(self, obj):
        return obj.remaining_time()

    def validate_code(self, value):
        if self.instance and self.instance.code == value:
            return value
            
        if Discount.objects.filter(code=value).exists():
            raise serializers.ValidationError("این کد تخفیف قبلاً استفاده شده است")
        return value

    def validate_percentage(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("درصد تخفیف باید بین 1 تا 100 باشد")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'seller'):
            validated_data['seller'] = request.user.seller
        return super().create(validated_data)
