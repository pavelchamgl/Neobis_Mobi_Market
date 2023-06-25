from django.urls import include, path, re_path
from rest_framework import routers

from .endpoints import UserCardItemViewSet, CardItemListAPIView, CardItemRetrieveAPIView

router = routers.DefaultRouter()
router.register('', UserCardItemViewSet, basename='my_products')

urlpatterns = [
    path('api/product/my/', include(router.urls)),
    path('api/product/list/', CardItemListAPIView.as_view()),
    re_path('api/product/(?P<id>.+)/', CardItemRetrieveAPIView.as_view()),
]
