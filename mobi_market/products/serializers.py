from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CardItem


class CardItemShortViewSerializers(ModelSerializer):
    class Meta:
        model = CardItem
        fields = ["id", "title", "price", "images", "short_description"]


class CardItemCRUDViewSetSerializer(ModelSerializer):
    class Meta:
        model = CardItem
        fields = ["id", "user_id", "title", "price", "images", "short_description", "detailed_description"]
