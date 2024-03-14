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
    image_ids = serializers.SerializerMethodField(read_only=True)

    def get_image_ids(self, obj):
        uploaded_image_ids = self.context.get('uploaded_image_ids', [])
        print(uploaded_image_ids)
        images = ServiceGalleryImage.objects.filter(id__in=uploaded_image_ids)
        return [[image.id, image.image] for image in images]
    # like_counter = serializers.SerializerMethodField(read_only=True)
    # view_counter = serializers.SerializerMethodField(read_only=True)
    # rate_point = serializers.DecimalField(source='user.rate_point', read_only=True,  max_digits=3, decimal_places=2)
    # user = UserSerializer(read_only=True)

    # @staticmethod
    # def get_like_counter(instance):
    #     return Like_Service.objects.filter(service=instance).count()

    # @staticmethod
    # def get_view_counter(instance):
    #     return View_Service.objects.filter(service=instance).count()
    
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
                  "image_ids",
                  "uploaded_images",
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