from rest_framework import serializers
from .models import Rate_User
from users.serializers import LikeToUserSerializer


class Rate_User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Rate_User
        fields = ["rated_user", "rate_number", "description", "image"]


class RatesFromUsersSerializer(serializers.ModelSerializer):
    rating_user = LikeToUserSerializer()

    class Meta:
        model = Rate_User
        fields = ["id", "rating_user", "rate_number", "description", "image", "date_created"]

    
class RateOfUserSerializer(serializers.ModelSerializer):
    rated_user = LikeToUserSerializer()

    class Meta:
        model = Rate_User
        fields = ["id", "rated_user", "rate_number", "description", "image", "date_created"]