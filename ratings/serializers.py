from rest_framework import serializers
from .models import Rate_User
from users.models import User


class User_CommentsSerializer(serializers.ModelSerializer):
    commented_user_username = serializers.SerializerMethodField(read_only=True)
    commented_user_avatar = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_commented_user_username(instance):
        return User.objects.get(id=instance.rating_user.id).username
    
    @staticmethod
    def get_commented_user_avatar(instance):
        return User.objects.get(id=instance.rating_user.id).avatar.url
    
    class Meta:
        model = Rate_User
        fields = "__all__"


class User_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar", "rate_point"]


class Leave_Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Rate_User
        fields = "__all__"