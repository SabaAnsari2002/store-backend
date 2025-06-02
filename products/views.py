from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category, Subcategory
from django.shortcuts import get_object_or_404
from .serializers import CategorySerializer, ProductSerializer, SubcategorySerializer
from rest_framework.views import APIView


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category', None)
        subcategory_name = self.request.query_params.get('subcategory', None)
        
        seller = self.request.user.seller
        queryset = queryset.filter(seller=seller)

        if category_name:
            queryset = queryset.filter(category__name=category_name)
        if subcategory_name:
            queryset = queryset.filter(subcategory__name=subcategory_name)
        
        return queryset

    def perform_create(self, serializer):
        seller = self.request.user.seller
        serializer.save(seller=seller)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], url_path='by-subcategory/(?P<subcategory_name>[^/]+)')
    def by_subcategory(self, request, subcategory_name=None):
        subcategory_name = subcategory_name.replace('-', ' ')
        subcategory = get_object_or_404(Subcategory, name=subcategory_name)
        products = Product.objects.filter(subcategory=subcategory)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_name>[^/]+)')
    def by_category(self, request, category_name=None):
        category_name = category_name.replace('-', ' ')
        category = get_object_or_404(Category, name=category_name)
        products = Product.objects.filter(category=category)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

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
