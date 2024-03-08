from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rate_User
from users.models import User
from django.http import Http404
from rest_framework import mixins, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class RatesFromView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404()
        rates = Rate_User.objects.filter(rated_user=user)
        rates_serialized = FromRateSerializer(rates, many=True)
        rated_user_serialized = RatedUserSerializer(user)
        return Response([rated_user_serialized.data, rates_serialized.data])


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
        rated_user.rate_point_total += serializer.validated_data.get('rate_number')
        rated_user.rate_point = rated_user.rate_point_total / rated_user.point_counter
        rated_user.save()
        self.perform_create(serializer, rating_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)