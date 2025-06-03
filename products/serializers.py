from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Subcategory, Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subcategory = serializers.CharField()
    category_id = serializers.SerializerMethodField()
    subcategory_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'category_id', 'subcategory_id', 'price', 'stock']
        read_only_fields = ['id']

    def get_category_id(self, obj):
        return obj.category.id if obj.category else None

    def get_subcategory_id(self, obj):
        return obj.subcategory.id if obj.subcategory else None

    def validate(self, data):
        category_name = data.get('category', '').strip()
        subcategory_name = data.get('subcategory', '').strip()
        product_name = data.get('name', '').strip()

        instance = getattr(self, 'instance', None)
        request = self.context.get('request')

        if category_name and subcategory_name and product_name:
            try:
                category = Category.objects.get(name=category_name)
                subcategory = Subcategory.objects.get(name=subcategory_name, category=category)
                
                query = Product.objects.filter(
                    name=product_name,
                    category=category,
                    subcategory=subcategory,
                    seller=request.user.seller
                )
                
                if instance:
                    query = query.exclude(pk=instance.pk)
                
                if query.exists():
                    raise ValidationError(
                        "محصولی با این نام، دسته‌بندی و زیردسته‌بندی از قبل وجود دارد."
                    )
                    
            except (Category.DoesNotExist, Subcategory.DoesNotExist):
                pass

        return data

    def create(self, validated_data):
        category_name = validated_data.pop('category', '').strip()
        subcategory_name = validated_data.pop('subcategory', '').strip()
        request = self.context.get('request')

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
            seller=request.user.seller,
            category=category,
            subcategory=subcategory,
            **validated_data
        )
        return product

    def update(self, instance, validated_data):
        category_name = validated_data.get('category', '').strip()
        subcategory_name = validated_data.get('subcategory', '').strip()
        request = self.context.get('request')

        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                print(f"دسته‌بندی '{category_name}' ایجاد شد.")
            instance.category = category

        if subcategory_name:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcategory_name, category=instance.category
            )
            if created:
                print(f"زیرمجموعه '{subcategory_name}' برای دسته‌بندی '{category_name}' ایجاد شد.")
            instance.subcategory = subcategory

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']