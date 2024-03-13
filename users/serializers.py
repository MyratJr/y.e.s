from .models import User
from ratings.models import Like_Service, Like_User, Rate_User
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.http import Http404
from services.models import Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email']


class UpdateUserOrGetListOfUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'banner_image', 'username', 'email', 'experience', 'address', 'summary', 'web', 'tiktok', 'instagram', 'imo', 'first_name', "last_name", 'phone']

    
class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'password', 'otp']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            phone=validated_data['phone']
        )
        return user


class ChangeForgotPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=4, write_only=True)
    class Meta:
        model = User
        fields = ['phone', 'password', 'otp']
        extra_kwargs = {'password': {'write_only': True}}
        

class UserViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                    "id", 
                    "username", 
                    "avatar", 
                    "first_name",
                    "last_name", 
                    "rate_point", 
                    "banner_image", 
                    "summary",
                    "phone", 
                    "experience", 
                    "address", 
                    "email", 
                    "web", 
                    "imo", 
                    "instagram", 
                    "tiktok",
                    "view_counter",
                    "like_counter"
                ]
    

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, attrs):
        if "+" in attrs.get('username'):
            try:
                username = User.objects.get(phone=attrs.get('username')).username
            except User.DoesNotExist:
                raise Http404()
        elif "@" in attrs.get('username'):
            try:
                username = User.objects.get(email=attrs.get('username')).username
            except User.DoesNotExist:
                raise Http404()
        else:
            try:
                username = attrs.get('username')
            except User.DoesNotExist:
                raise Http404()
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

class LikeFromUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'avatar')


class LikeToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)

class LikedUsersSerializer(serializers.ModelSerializer):
    favoriting_user = LikeFromUserSerializer()
    favorited_user = LikeToUserSerializer()
    
    class Meta:
        model = Like_User
        fields = "__all__"
        depth = 1


class RateSerializer(serializers.ModelSerializer):
    rating_user = LikeFromUserSerializer()
    rated_user = LikeToUserSerializer()

    class Meta:
        model = Rate_User
        fields = '__all__'
        depth = 1


class RateOfUserSerializer(serializers.ModelSerializer):
    rating_user = LikeToUserSerializer()
    rated_user = LikeFromUserSerializer()

    class Meta:
        model = Rate_User
        fields = '__all__'
        depth = 1

class LikeToServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'primary_image')


class LikedServiceSerializer(serializers.ModelSerializer):
    user = LikeFromUserSerializer()
    service = LikeToServiceSerializer()

    class Meta:
        model = Like_Service
        fields = '__all__'
        depth = 1


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)