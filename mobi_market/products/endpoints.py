from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CardItem
from .serializers import CardItemShortViewSerializers, CardItemCRUDViewSetSerializer


class UserCardItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CardItemShortViewSerializers

    @swagger_auto_schema(
        operation_description="This endpoint return all user products.",
        responses={
            200: CardItemShortViewSerializers,
            400: 'Bad Request'
        }
    )
    def get_queryset(self):
        user = self.request.user
        queryset = CardItem.objects.filter(user_id=user.id)
        return queryset

    @swagger_auto_schema(
        request_body=CardItemCRUDViewSetSerializer,
        operation_description="This endpoint create user product.",
        responses={
            201: 'serializer.data',
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data["user_id"] = user.id
        serializer = CardItemCRUDViewSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=CardItemCRUDViewSetSerializer,
        operation_description="This endpoint update user product.",
        responses={
            201: 'serializer.data',
            400: 'Bad Request'
        }
    )
    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = CardItemCRUDViewSetSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="This endpoint retrieve user product.",
        responses={
            201: CardItemCRUDViewSetSerializer,
            400: 'Bad Request'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CardItemCRUDViewSetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardItemListAPIView(ListAPIView):
    queryset = CardItem.objects.all()
    serializer_class = CardItemShortViewSerializers
    permission_classes = [IsAuthenticated]


class CardItemRetrieveAPIView(RetrieveAPIView):
    queryset = CardItem.objects.all()
    serializer_class = CardItemCRUDViewSetSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
