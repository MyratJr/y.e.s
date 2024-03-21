from rest_framework import status
from rest_framework.response import Response
from .serializers import OTPSerializer, SMSSerializer, OTPVerifySerializer
from random import randint
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import User
from ehyzmat.settings import redis_cache
from rest_framework.views import APIView
from .models import Otp, SMSStatuses
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


class ResendOTPORForgotPasswordView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = randint(1000,9999)
        redis_cache.set(phone, otp, ex=300)
        phone_obj, created = Otp.objects.get_or_create(phone=phone)
        phone_obj.message = f"Siziň Y.E.S barlag koduňyz: {otp}"
        phone_obj.status = SMSStatuses.PENDING
        phone_obj.each_counter = 0
        phone_obj.all_counter = 0
        phone_obj.save()
        return Response(status=status.HTTP_201_CREATED)
    

class SMSPhoneView(APIView):
    serializer_class = SMSSerializer
    permission_classes = [IsAdminUser]
    queryset = Otp.objects.filter(each_counter=0, status=SMSStatuses.PENDING)

    def get(self, request):
        sms = self.queryset.first()

        if sms:
            sms.tried()
            sms.save()
            serializer = self.serializer_class(instance=sms,
                                               context={"request": request})

            return Response(serializer.data)
        return Response({"id": 0})
    @extend_schema(
        description="Eger Telefon belgä sms giden bolsa message forumy 1 bilen iberiň, eger gitmedik bolsa 0 bilen iberiň.",
        request=SMSSerializer,
    )
    def post(self, request):
        phone = request.data.get("phone")
        status = request.data.get("message")
        phone = str(phone)
        status = int(status)
        if status == 1:
            self.queryset.filter(phone=phone, status=SMSStatuses.PENDING) \
                .update(status=SMSStatuses.DELIVERED)
        elif status == 0:
            self.queryset.filter(phone=phone, status=SMSStatuses.PENDING) \
                            .update(each_counter=0)
        return Response({})
    

class ActivateUserAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=OTPVerifySerializer,
    )
    def post(self, request):
        otp = request.data.get("otp")
        phone = request.data.get('phone')

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