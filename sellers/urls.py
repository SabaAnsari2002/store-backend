from django.urls import path
from .views import SellerRegister, SellerLogin, Check_shop

urlpatterns = [
    path('register/', SellerRegister.as_view()),
    path('login/', SellerLogin.as_view()),
    path('check-shop/', Check_shop , name='check_shop'),
]