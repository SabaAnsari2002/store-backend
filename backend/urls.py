from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, LoginView
from sellerpanel.views import dashboard, product_list, edit_product, delete_product, order_list, delete_order, update_order_status , order_detail



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),

    path('products/', product_list, name='product_list'),
    path('products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),

    path('orders/', order_list, name='order_list'),
    path('orders/delete/<int:pk>/', delete_order, name='delete_order'),
    path('orders/update/<int:pk>/', update_order_status, name='update_order_status'),
    path('orders/detail/<int:pk>/', order_detail, name='order_detail'),
]