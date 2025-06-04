from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category, Subcategory
from django.shortcuts import get_object_or_404
from .serializers import CategorySerializer, ProductSerializer, SubcategorySerializer
from rest_framework.views import APIView
from sellers.serializers import SellerSerializer 
from django.db.models import Min, Count


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'seller'):
            queryset = queryset.filter(seller=self.request.user.seller)
            return queryset
        
        if self.action == 'list':
            distinct_products = Product.objects.values(
                'name', 'category', 'subcategory'
            ).annotate(
                min_id=Min('id'),
                sellers_count=Count('id', distinct=True)
            ).order_by('name')

            product_ids = [p['min_id'] for p in distinct_products]
            queryset = queryset.filter(id__in=product_ids)
        
        category_name = self.request.query_params.get('category')
        subcategory_name = self.request.query_params.get('subcategory')
        
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        if subcategory_name:
            queryset = queryset.filter(subcategory__name=subcategory_name)
        
        return queryset

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'seller'):
            raise PermissionError("فقط فروشندگان می‌توانند محصول ایجاد کنند.")
        serializer.save()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], url_path='by-subcategory/(?P<subcategory_name>[^/]+)')
    def by_subcategory(self, request, subcategory_name=None):
        subcategory_name = subcategory_name.replace('-', ' ')
        subcategory = get_object_or_404(Subcategory, name=subcategory_name)
        distinct_products = Product.objects.filter(
            subcategory=subcategory
        ).values(
            'name', 'category', 'subcategory'
        ).annotate(
            min_id=Min('id')
        )
        
        product_ids = [p['min_id'] for p in distinct_products]
        products = Product.objects.filter(id__in=product_ids, subcategory=subcategory)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_name>[^/]+)')
    def by_category(self, request, category_name=None):
        category_name = category_name.replace('-', ' ')
        category = get_object_or_404(Category, name=category_name)
        distinct_products = Product.objects.filter(
            category=category
        ).values(
            'name', 'category', 'subcategory'
        ).annotate(
            min_id=Min('id')
        )
        
        product_ids = [p['min_id'] for p in distinct_products]
        products = Product.objects.filter(id__in=product_ids, category=category)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='sellers')
    def product_sellers(self, request, pk=None):
        product = self.get_object()
        similar_products = Product.objects.filter(
            name=product.name,
            category=product.category,
            subcategory=product.subcategory
        ).select_related('seller')
        
        sellers_data = []
        for p in similar_products:
            sellers_data.append({
                'seller': SellerSerializer(p.seller, context={'request': request}).data,
                'price': p.price,
                'stock': p.stock,
                'product_id': p.id
            })
        
        return Response(sellers_data)

class CategoryListAPIView(APIView):
    def get(self, request, category_name=None):
        category = get_object_or_404(Category, name=category_name)  
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryListAPIView(APIView):
    def get(self, request, subcategory_name=None):
        subcategory = get_object_or_404(Subcategory, name=subcategory_name)  
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)