from django.urls import include, path, re_path
from rest_framework import routers

from .endpoints import UserCardItemViewSet, CardItemListAPIView, CardItemRetrieveAPIView, CardItemLikeAPIView, CardItemUnlikeAPIView, FavouriteCardItemListApiView, FavouriteCardItemRetrieveApiView

router = routers.DefaultRouter()
router.register('', UserCardItemViewSet, basename='my_products')

urlpatterns = [
    path('api/products/my/', include(router.urls)),
    path('api/products/all/', CardItemListAPIView.as_view()),
    re_path('api/product/(?P<id>.+)/', CardItemRetrieveAPIView.as_view()),
    re_path('api/like/(?P<product_id>.+)/product/', CardItemLikeAPIView.as_view(), name='card_item_like'),
    re_path('api/unlike/(?P<product_id>.+)/product/', CardItemUnlikeAPIView.as_view(), name='card_item_unlike'),
    path('api/favourite_products/list/', FavouriteCardItemListApiView.as_view()),
    re_path('api/favourite_product/(?P<pk>.+)/', FavouriteCardItemRetrieveApiView.as_view()),
]
