from rest_framework import serializers
from .models import Service, ServiceGalleryImage, Service_Category
from advertisement.models import Advertisement
from ratings.models import Like_Service, View_Service
from users.models import User

class ServiceGalleryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceGalleryImage
        fields = ["image"]


class ServicesSerializers(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(write_only=True)
    like_counter = serializers.SerializerMethodField(read_only=True)
    view_counter = serializers.SerializerMethodField(read_only=True)
    rate_point = serializers.SerializerMethodField(read_only=True)
    user = serializers.IntegerField(read_only=True)

    @staticmethod
    def get_like_counter(instance):
        return Like_Service.objects.filter(service=instance).count()

    @staticmethod
    def get_view_counter(instance):
        return View_Service.objects.filter(service=instance).count()
    
    @staticmethod
    def get_rate_point(request):
        return User.objects.get(pk=request.user).rate_point
    
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
                  "uploaded_images",
                  "rate_point",
                  "view_counter",
                  "like_counter",
                ]
    

    def create(self, validated_data):
        uploaded_images_id = validated_data.pop("uploaded_images")
        new_service = Service.objects.create(**validated_data)
        string = str(uploaded_images_id)
        inner_string = string[2:-2]
        uploaded_images_id = eval(inner_string)  
        for image_id in uploaded_images_id:
            relating_image = ServiceGalleryImage.objects.get(id=image_id)
            relating_image.product = new_service
            relating_image.save()
        return new_service
    
    def update(self, instance, validated_data):
        uploaded_images_id = validated_data.pop("uploaded_images")
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        string = str(uploaded_images_id)
        inner_string = string[2:-2]
        uploaded_images_id = eval(inner_string)  
        for image_id in uploaded_images_id:
            relating_image = ServiceGalleryImage.objects.get(id=image_id)
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