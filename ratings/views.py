from rest_framework import mixins, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from users.models import User
from .models import Rate_User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class RateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Rate_User_Serializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rated_user = serializer.validated_data.get('rated_user')
        rated_user = get_object_or_404(User, id=rated_user.id)
        rated_user.point_counter += 1
        rate_number = serializer.validated_data.get('rate_number')
        rated_user.rate_point_total += rate_number
        rated_user.rate_point = rated_user.rate_point_total / rated_user.point_counter
        rated_user.save()
        self.perform_create(serializer)
        return Response("Rate created successfully", status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(rating_user=self.request.user)


class RatesFromUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rated_users = Rate_User.objects.filter(rated_user=request.user)
        rated_serializer = RatesFromUsersSerializer(rated_users, many=True)
        return Response(rated_serializer.data, status=status.HTTP_200_OK)
    

class RatesToUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rating_users = Rate_User.objects.filter(rating_user=request.user)
        rating_serializer = RateOfUserSerializer(rating_users, many=True)
        return Response(rating_serializer.data, status=status.HTTP_200_OK)