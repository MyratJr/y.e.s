from rest_framework import serializers
from .models import Otp

class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(read_only=True)
    phone = serializers.CharField()


class SMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otp
        fields = ["phone", "message"]