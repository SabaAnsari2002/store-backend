from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryListAPIView, SubcategoryListAPIView
from django.urls import path,re_path

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')
urlpatterns = [
    path('api/categories/<str:category_name>/', CategoryListAPIView.as_view(), name='category-detail'),
    path('api/subcategories/<str:subcategory_name>/', SubcategoryListAPIView.as_view(), name='subcategory-detail'),
]
urlpatterns = router.urls