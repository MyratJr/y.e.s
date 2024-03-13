from rest_framework import mixins, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from users.models import User
from .models import Rate_User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class RateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Rate_User_Serializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rated_user = serializer.validated_data.get('rated_user')
        rated_user = get_object_or_404(User, pk=rated_user.id)
        rated_user.point_counter += 1
        rate_number = serializer.validated_data.get('rate_number')
        rated_user.rate_point_total += rate_number
        rated_user.rate_point = rated_user.rate_point_total / rated_user.point_counter
        rated_user.save()
        self.perform_create(serializer)

    def perform_create(self, serializer):
        serializer.save(rating_user=self.request.user)

        # Rate_User.objects.create(
        #     rating_user=request.user,
        #     rated_user=rated_user,
        #     rate_number=rate_number,
        #     description=serializer.validated_data.get('description'),
        #     image=serializer.validated_data.get('image')
        # )
        return Response("Rate created successfully", status=status.HTTP_201_CREATED)