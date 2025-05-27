from rest_framework import serializers
from .models import Product, Category, Subcategory

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subcategory = serializers.CharField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'price', 'stock']
        read_only_fields = ['id']

    def create(self, validated_data):
        category_name = validated_data.pop('category', '').strip()
        subcategory_name = validated_data.pop('subcategory', '').strip()

        category = Category.objects.filter(name__iexact=category_name).first()
        if not category:
            raise serializers.ValidationError(f"دسته‌بندی '{category_name}' یافت نشد.")

        subcategory = Subcategory.objects.filter(name__iexact=subcategory_name, category=category).first()
        if not subcategory:
            raise serializers.ValidationError(f"زیرمجموعه '{subcategory_name}' برای دسته‌بندی '{category_name}' یافت نشد.")

        product = Product.objects.create(
            seller=self.context['request'].user.seller,
            category=category,
            subcategory=subcategory,
            **validated_data
        )
        return product

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        subcategory_name = validated_data.pop('subcategory', None)

        if category_name:
            category = Category.objects.filter(name__iexact=category_name.strip()).first()
            if not category:
                raise serializers.ValidationError(f"دسته‌بندی '{category_name}' نامعتبر است.")
            instance.category = category

        if subcategory_name:
            subcategory = Subcategory.objects.filter(name__iexact=subcategory_name.strip(), category=instance.category).first()
            if not subcategory:
                raise serializers.ValidationError(f"زیرمجموعه '{subcategory_name}' برای این دسته یافت نشد.")
            instance.subcategory = subcategory

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name if instance.category else None
        data['subcategory'] = instance.subcategory.name if instance.subcategory else None
        return data
