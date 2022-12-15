from rest_framework import serializers
from hotel.models import Dishes
from django.contrib.auth.models import User
from hotel.models import Review


class DishSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()


class DishesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"

    def validate(self, data):
        price = data.get("price")
        if price < 0:
            raise serializers.ValidationError("invalid price")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    dish = DishesModelSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = [

            'dish',
            'rating',
            'comment',
            'created_date'
        ]

    def create(self, validated_data):

        user = self.context.get("user")
        dish = self.context.get("dish")
        return Review.objects.create(user=user, dish=dish, **validated_data)
