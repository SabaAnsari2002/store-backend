from django.urls import path
from .views import SellerRegister, SellerLogin

urlpatterns = [
    path('register/', SellerRegister.as_view()),
    path('login/', SellerLogin.as_view()),
]