from rest_framework import serializers
from .models import Category, Subcategory, Product

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

        category, created = Category.objects.get_or_create(name=category_name)
        if created:
            print(f"دسته‌بندی '{category_name}' ایجاد شد.")
        
        subcategory, created = Subcategory.objects.get_or_create(
            name=subcategory_name, category=category
        )
        if created:
            print(f"زیرمجموعه '{subcategory_name}' برای دسته‌بندی '{category_name}' ایجاد شد.")

        validated_data.pop('seller', None)

        product = Product.objects.create(
            seller=self.context['request'].user.seller,
            category=category,
            subcategory=subcategory,
            **validated_data
        )
        return product

    def update(self, instance, validated_data):
        category_name = validated_data.get('category', '').strip()
        subcategory_name = validated_data.get('subcategory', '').strip()

        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            instance.category = category

        if subcategory_name:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcategory_name, category=instance.category
            )
            instance.subcategory = subcategory

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']