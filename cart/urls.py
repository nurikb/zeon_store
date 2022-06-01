from django.urls import path
from .views import AddToCart, CartInfo, CartRemove, FavoriteInfo, AddToFavorite, FavoriteRemove

app_name = 'cart'

urlpatterns = [
    path('cart/add/<int:pk>/', AddToCart.as_view(), name='cart_add'),
    path('cart/remove/<int:pk>/', CartRemove.as_view(), name='cart_remove'),
    path('cart/', CartInfo.as_view(), name='cart_info'),
    # path('favorite/<int:pk>/', AddToFavorite.as_view()),
    # path('favorite/', FavoriteInfo.as_view()),
    # path('favorite/remove/<int:pk>/', FavoriteRemove.as_view()),
]