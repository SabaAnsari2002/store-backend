from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryListAPIView, SubcategoryListAPIView
from django.urls import path,re_path

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [
    path('api/categories/<str:category_name>/', CategoryListAPIView.as_view(), name='category-detail'),
    path('api/subcategories/<str:subcategory_name>/', SubcategoryListAPIView.as_view(), name='subcategory-detail'),
    path('api/products/<int:pk>/update-stock/', ProductViewSet.as_view({'patch': 'update_stock'}), name='product-update-stock'),
    path('api/products/<int:pk>/stock/', ProductViewSet.as_view({'patch': 'update_stock'}), name='product-stock'),

]

urlpatterns += router.urls