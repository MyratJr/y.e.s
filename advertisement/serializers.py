from rest_framework import serializers
from .models import Advertisement


class HomeAdvertisementsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all__'