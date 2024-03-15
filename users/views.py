from rest_framework.generics import GenericAPIView
from rest_framework import generics, permissions, mixins, viewsets
from services.serializers import HomeServicesSerializers
from ratings.models import Like_User, View_User
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from services.models import Service
from .serializers import *
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from ehyzmat.settings import redis_cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import OrderingFilter


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        otp = str(serializer.validated_data["otp"])
        temporary_otp = redis_cache.get(phone)
        if temporary_otp and temporary_otp.decode() == otp:
            redis_cache.delete(phone)
            user = serializer.save()
            refresh = RefreshToken.for_user(User.objects.get(id=user.id))
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response("OTP is wrong or has expired", status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeForgotPassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ChangeForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser]
    queryset = User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        otp = data.get("otp")
        phone = data.get("phone")
        password = data.get("password")
        temporary_otp = redis_cache.get(phone)
        if temporary_otp and temporary_otp.decode() == otp:
            redis_cache.delete(phone)
            user_change_password = User.objects.get(phone=phone)
            user_change_password.set_password(password)
            user_change_password.save()
            return Response({"success"})
        raise serializers.ValidationError({"detail":"Your OTP is wrong or has expired"})


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(User.objects.get(id=user.id))
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    

class UpdateUserAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserOrGetListOfUsersSerializer
    parser_classes = [MultiPartParser,FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save() 

class ListUsersView(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserOrGetListOfUsersSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserProfileView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        services = Service.objects.filter(user=instance, public=True)
        if request.user and request.user.is_authenticated:
            service, created = View_User.objects.get_or_create(viewing_user=request.user, viewed_user=instance)
            if created:
                instance.view_counter = instance.view_counter + 1
                instance.save()
        new_data = [{"User_data": serializer.data}, {
                    "User_services": HomeServicesSerializers(services, many=True).data,
                    }]
        return Response(new_data)


class UserProfilServicesView(generics.RetrieveAPIView):
    serializer_class = HomeServicesSerializers
    permission_classes = [permissions.AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["user__rate_point", "experience"]

    def get_queryset(self):
        queryset = Service.objects.filter(user=self.kwargs['pk'])
        return queryset


class LikeUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        liked_user = get_object_or_404(User, pk=pk)
        user, created = Like_User.objects.get_or_create(favoriting_user=request.user,favorited_user=liked_user)
        if created:
            liked_user.like_counter += 1
            liked_user.save()
            return Response({"success": True, "likes": liked_user.like_counter})
        return Response({"success": True, "likes": 0})


class LikesFromUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_users = Like_User.objects.filter(favorited_user=request.user)
        liked_serializer = LikesFromUsersSerializer(liked_users, many=True)
        return Response(liked_serializer.data, status=status.HTTP_200_OK)
    

class LikesToUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liking_users = Like_User.objects.filter(favoriting_user=request.user)
        liking_serializer = LikesToUsersSerializer(liking_users, many=True)
        return Response(liking_serializer.data, status=status.HTTP_200_OK)
    

class ServiceLikesFromUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_liked_services = Like_Service.objects.filter(service__user=request.user).select_related("user", "service")
        my_liked_sevices_serializer = ServiceLikesFromUsersSerializer(my_liked_services, many=True)
        return Response(my_liked_sevices_serializer.data, status=status.HTTP_200_OK)
    

class LikesToServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_liking_services = Like_Service.objects.filter(user=request.user)
        my_liking_sevices_serializer = LikesToServiceSerializer(my_liking_services, many=True)
        return Response(my_liking_sevices_serializer.data, status=status.HTTP_200_OK)