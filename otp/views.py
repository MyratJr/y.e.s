from rest_framework import status
from rest_framework.response import Response
from .serializers import OTPSerializer, SMSSerializer
from random import randint
from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import User
from ehyzmat.settings import redis_cache
from rest_framework.views import APIView
import json
from otp.models import Otp, SMSStatuses
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class OTPView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = randint(1000,9999)
        redis_cache.set(phone, otp, ex=60)
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
    

class SMSPhoneView(APIView):
    serializer_class = SMSSerializer
    permission_classes = [AllowAny]
    queryset = Otp.objects.filter(status=SMSStatuses.PENDING)

    def get(self, request):
        sms = self.queryset.first()

        if sms:
            sms.tried()
            sms.status=SMSStatuses.SENT
            sms.save()
            serializer = self.serializer_class(instance=sms,
                                               context={"request": request})

            return Response(serializer.data)
        return Response({"id": 0})

    def post(self, request):
        phone = request.data.get("phone", "")
        phone = str(phone)
        Otp.objects.filter(phone=phone, status=SMSStatuses.SENT) \
            .update(status=SMSStatuses.DELIVERED)
        return Response({})
    

class ActivateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp = request.data.get("otp", "")
        phone = request.data.get('phone', "")

        if otp == '':
            return Response({'error': 'Kody giriziň'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sms = Otp.objects.filter(phone=phone, status=SMSStatuses.DELIVERED).latest('date_created')
        except Otp.DoesNotExist:
            return Response({'error': 'Bu nomera degişli kod ýok'},
                            status=status.HTTP_404_NOT_FOUND)

        if otp != redis_cache.get(phone).decode("utf-8"):
            return Response({'error': 'Ýalňyş kod'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
            user.is_active = True
            user.last_login = timezone.now()
            user.save()

            sms.status = SMSStatuses.ACTIVATED
            sms.message = "Y.E.S platformasyna hoş geldiňiz!"
            sms.save()

            refresh = RefreshToken.for_user(User.objects.get(id=user.id))
            return Response(
                {
                    'message': 'Success',
                    'user': {
                        'id': user.id,
                        'phone': user.phone
                    },
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                },
                status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Error'},
                            status=status.HTTP_404_NOT_FOUND)