from django.urls import path
from .views import SellerRegister, SellerLogin, Check_shop, UserProfileView

urlpatterns = [
    path('register/', SellerRegister.as_view()),
    path('login/', SellerLogin.as_view()),
    path('check-shop/', Check_shop , name='check_shop'),
    path('issellers/', UserProfileView.as_view(), name='user_profile'),
]