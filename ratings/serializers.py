from rest_framework import serializers
from .models import Rate_User


class Rate_User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Rate_User
        fields = ["rated_user", "rate_number", "description", "image"]