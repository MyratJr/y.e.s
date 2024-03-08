from rest_framework import serializers
from .models import Rate_User
from users.models import User


class FromRateSerializer(serializers.ModelSerializer):
    rater_username = serializers.SerializerMethodField(read_only=True)
    rater_avatar = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_rater_username(instance):
        return User.objects.get(id=instance.rating_user.id).username
    
    @staticmethod
    def get_rater_avatar(instance):
        return User.objects.get(id=instance.rating_user.id).avatar.url
    
    class Meta:
        model = Rate_User
        fields = "__all__"


class RatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar", "rate_point"]


class Rate_User_Serializer(serializers.ModelSerializer):
    rating_user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rate_User
        fields = ["rated_user", "rate_number", "description", "image"]