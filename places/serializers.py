from rest_framework import serializers
from .models import Regions, Districts


class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = ["id", "district"]


class RegionsSerializer(serializers.ModelSerializer):
    region_district = DistrictsSerializer(many=True)

    class Meta:
        model = Regions
        fields = ['name', 'region_district']
