from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView

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
            201: 'Product added successfully.',
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data["user_id"] = user.id
        serializer = CardItemCRUDViewSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product added successfully.'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=CardItemCRUDViewSetSerializer,
        operation_description="This endpoint update user product.",
        responses={
            201: 'Product update successfully.',
            400: 'Bad Request'
        }
    )
    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = CardItemCRUDViewSetSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product update successfully.'}, status=status.HTTP_200_OK)

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


class CardItemLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        user = request.user
        if not user.phone_number:
            return Response({'message': 'To add to your favorites, you need to confirm your phone number.'})
        try:
            card_item = CardItem.objects.get(id=product_id)
        except card_item.DoesNotExist:
            return Response({'error': 'Card item not found.'}, status=status.HTTP_404_NOT_FOUND)
        if card_item.likes.filter(id=user.id).exists():
            return Response({'message': 'You have already liked this product.'}, status=status.HTTP_400_BAD_REQUEST)
        card_item.likes.add(user.id)
        return Response({'message': 'Product liked successfully.'}, status=status.HTTP_200_OK)


class CardItemUnlikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        user = request.user
        if not user.phone_number:
            return Response({'message': 'To add to your favorites, you need to confirm your phone number.'})
        try:
            card_item = CardItem.objects.get(id=product_id)
        except card_item.DoesNotExist:
            return Response({'error': 'Card item not found'}, status=status.HTTP_404_NOT_FOUND)
        if not card_item.likes.filter(id=user.id).exists():
            return Response({'message': 'You not liked this product.'}, status=status.HTTP_400_BAD_REQUEST)
        card_item.likes.remove(user.id)
        return Response({'success': 'User succesfully deleted from likes'})


class FavouriteCardItemListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardItemShortViewSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = CardItem.objects.filter(likes__id=user_id)
        return queryset


class FavouriteCardItemRetrieveApiView(RetrieveAPIView):
    serializer_class = CardItemCRUDViewSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = CardItem.objects.filter(likes__id=user_id)
        return queryset
