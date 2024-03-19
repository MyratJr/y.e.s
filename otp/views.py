from rest_framework import status
from rest_framework.response import Response
from .serializers import OTPSerializer
from random import randint
from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from ehyzmat.settings import redis_cache
from rest_framework.views import APIView


class OTPView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = randint(1000,9999)
        redis_cache.set(phone, otp, ex=300)
        return Response(status=status.HTTP_201_CREATED)
    

class ForgotPasswordView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        try: 
            User.objects.get(phone=phone)
        except:
            return Response({"No user found with this phone!"})
        otp = randint(1000,9999)
        redis_cache.set(phone, otp, ex=300)
        return Response(status=status.HTTP_201_CREATED)
    

class ListPhoneNumbersView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        phone_numbers = []
        for key, value in redis_cache.items():
            if isinstance(value, int):
                phone_numbers.append({'phone_number': key, 'otp': value})
        return Response(phone_numbers)