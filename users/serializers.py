from rest_framework import serializers
from .models import CustomUser
from .models import Address


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
            'new_password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)

        # Verify current password if changing password
        if new_password:
            if not password:
                raise serializers.ValidationError({"password": "Current password is required to set a new password."})
            if not instance.check_password(password):
                raise serializers.ValidationError({"password": "Current password is incorrect."})
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
