from rest_framework import viewsets, permissions
from .models import Product, Category, Subcategory
from .serializers import ProductSerializer,CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        subcategory_id = self.request.query_params.get('subcategory', None)

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset

    def perform_create(self, serializer):
        seller = self.request.user.seller
        serializer.save(seller=seller)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
