from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer
from .models import User


class UserCreateAPIView(APIView):

    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        operation_description="This endpoint create user.",
        responses={201: 'User create successfully', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        User.objects.create_user(user_data["username"], user_data["email"], user_data["password"])
        return Response(
            {'message': 'User create successfully'}, status=status.HTTP_201_CREATED
        )

