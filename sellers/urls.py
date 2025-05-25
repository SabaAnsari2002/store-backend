from django.urls import path
from .views import SellerRegister

urlpatterns = [
    path('register/', SellerRegister.as_view()),
]