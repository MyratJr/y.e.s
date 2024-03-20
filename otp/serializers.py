from rest_framework import serializers
from .models import Otp

class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField()


class SMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otp
        fields = ["phone", "message"]