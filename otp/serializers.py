from rest_framework import serializers


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(read_only=True)
    phone = serializers.CharField()