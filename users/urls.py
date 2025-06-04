from django.urls import path
from .views import RegisterUser, UserProfileView, AddressListCreateView,AddressRetrieveUpdateDestroyView,SetDefaultAddressView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('addresses/', AddressListCreateView.as_view(), name='address_list_create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyView.as_view(), name='address_detail'),
    path('addresses/<int:pk>/set_default/', SetDefaultAddressView.as_view(), name='set_default_address'),
]
