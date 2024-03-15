from rest_framework import serializers
from .models import Service, ServiceGalleryImage, Service_Category
from advertisement.models import Advertisement
from ratings.models import Like_Service, View_Service
from users.models import User

class ServiceGalleryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceGalleryImage
        fields = ["id", "image"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "avatar", "rate_point", "phone", "email", "web", "imo", "instagram", "tiktok") 


class ServicesSerializers(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(write_only=True)
    image_url = serializers.SerializerMethodField('get_image_url', read_only=True)

    def get_image_url(self, obj):
        uploaded_images = [image.id for image in obj.images.all()]
        return [[i.id, str(i.image.url)] for i in ServiceGalleryImage.objects.filter(id__in=uploaded_images)]
    
    class Meta:
        model = Service
        fields = ["id",
                  "user", 
                  "name", 
                  "price", 
                  "category", 
                  "place", 
                  "experience", 
                  "description", 
                  "primary_image", 
                  "image_url",
                  "uploaded_images",
                  "view_counter",
                  "like_counter",
                ]
    

    def create(self, validated_data):
        uploaded_images_id = validated_data.pop("uploaded_images")
        new_service = Service.objects.create(**validated_data)
        for relating_image in ServiceGalleryImage.objects.filter(id__in=eval(uploaded_images_id[0])):
            relating_image.product = new_service
            relating_image.save()
        return new_service
    
    def update(self, instance, validated_data):
        uploaded_images_id = validated_data.pop("uploaded_images")
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        for relating_image in ServiceGalleryImage.objects.filter(id__in=eval(uploaded_images_id[0])):
            relating_image.product = instance
            relating_image.save()
        return instance
    

class HomeServicesSerializers(serializers.ModelSerializer):
    # liked_count = serializers.SerializerMethodField()
    # viewed_count = serializers.SerializerMethodField()

    # @staticmethod
    # def get_liked_count(instance):
    #     return Like_Service.objects.filter(service=instance).count()

    # @staticmethod
    # def get_viewed_count(instance):
    #     return View_Service.objects.filter(service=instance).count()
    
    class Meta:
        model = Service
        fields = '__all__'


class HomeCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service_Category
        fields = '__all__'


class HomeAdvertisementsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'