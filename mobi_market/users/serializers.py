from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User


class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(required=True, max_length=128, min_length=6, write_only=True)
    password_repeat = serializers.CharField(max_length=128, min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_repeat"]

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')
        if password != password_repeat:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "avatar", "birth_date", "phone_number"]


class PhoneNumberSerializer(ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ["phone_number"]
