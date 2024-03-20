from rest_framework import status
from rest_framework.response import Response
from .serializers import OTPSerializer, SMSSerializer
from random import randint
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import User
from rest_framework.parsers import MultiPartParser
from ehyzmat.settings import redis_cache
from rest_framework.views import APIView
from .models import Otp, SMSStatuses
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ResendOTPView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = randint(1000,9999)
        redis_cache.set(phone, otp)
        phone = Otp.objects.get_or_create(phone=phone)
        phone.message = f"Siziň barlag koduňyz: {otp}"
        phone.status = SMSStatuses.PENDING
        phone.save()
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
    permission_classes = [IsAdminUser]
    queryset = Otp.objects.filter(status=SMSStatuses.PENDING)

    def get(self, request):
        sms = self.queryset.first()

        if sms:
            sms.tried()
            sms.save()
            serializer = self.serializer_class(instance=sms,
                                               context={"request": request})

            return Response(serializer.data)
        return Response({"id": 0})
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone'],
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):
        phone = request.data.get("phone", "")
        phone = str(phone)
        self.queryset.filter(phone=phone, status=SMSStatuses.PENDING) \
            .update(status=SMSStatuses.DELIVERED)
        return Response({})
    

class ActivateUserAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone'],
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone for activate user'),
            }
        )
    )
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