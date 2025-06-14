from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, UserOrdersView

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('checkout/', OrderViewSet.as_view({'post': 'checkout'}), name='order-checkout'),
    path('<int:pk>/details/', OrderViewSet.as_view({'get': 'details'}), name='order-details'),
    path('history/', OrderViewSet.as_view({'get': 'order_history'}), name='order-history'),
    path('orders/by-seller/', OrderViewSet.as_view({'get': 'orders_by_seller'})),
    path('by-user/', UserOrdersView.as_view(), name='user-orders'),
] + router.urls