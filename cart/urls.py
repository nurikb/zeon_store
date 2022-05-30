from django.urls import path
from .views import AddToCart, CartInfo, CartRemove

app_name = 'cart'

urlpatterns = [
    path('add/<int:pk>/', AddToCart.as_view(), name='cart_add'),
    path('remove/<int:pk>/', CartRemove.as_view(), name='cart_remove'),
    path('', CartInfo.as_view(), name='cart_info'),
]