from random import choices
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .services import send_verification_code
from .serializers import UserCreateSerializer, UserProfileSerializer, PhoneNumberSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        operation_description="This endpoint create user.",
        responses={
            201: 'User create successfully',
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint return user profile.",
        responses={
            200: UserProfileSerializer,
            400: 'Bad Request'
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        operation_description="This endpoint update user profile.",
        responses={
            200: 'User profile update successfully',
            400: 'Bad Request'
        }
    )
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Personal info added successfully.'}, status=status.HTTP_200_OK)


class SetPhoneNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PhoneNumberSerializer,
        operation_description="This endpoint set user phone number.",
        responses={
            200: 'Phone number added successfully and verification code has been sent to your phone number.',
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = PhoneNumberSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        activation_code = "".join(choices("0123456789", k=4))
        user.activation_code = activation_code
        user.save()
        phone_number = user.phone_number
        send_verification_code(phone_number, activation_code)
        return Response(
            {'message': 'Phone number added successfully and verification code has been sent to your phone number.'},
            status=status.HTTP_200_OK
        )


class PhoneNumberActivateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint verify code from user phone number.",
        responses={
            200: 'Phone number verified successfully.',
            400: 'Please enter the correct verification code.'
        }
    )
    def post(self, request):
        user = request.user
        activation_code = request.data.get('activation_code')
        if activation_code == user.activation_code:
            user.is_verified = True
            user.save()
            return Response(
                {'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Please enter the correct verification code.'}, status=status.HTTP_400_BAD_REQUEST
            )
