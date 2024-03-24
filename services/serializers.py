from rest_framework import serializers
from .models import Service, ServiceGalleryImage, Service_Category
from ratings.models import Like_Service
from users.models import User
from users.serializers import LikeToUserSerializer


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
    gallery_images = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    view_counter = serializers.IntegerField(read_only=True)
    like_counter = serializers.IntegerField(read_only=True)
    category_get = serializers.CharField(source='category.name', read_only=True)
    place_get = serializers.CharField(source='place.district', read_only=True)
    category = serializers.CharField(write_only=True)
    place = serializers.CharField(write_only=True)

    def get_user(self, obj):
        request = self.context["request"]
        return {
            "id": obj.user.id,
            'username': obj.user.username,
            'avatar': request.build_absolute_uri(obj.user.avatar.url)
        }


    def get_gallery_images(self, obj):
        request = self.context["request"]
        uploaded_images = [image.id for image in obj.images.all()]
        return [{"id":i.id, "image":request.build_absolute_uri(i.image.url)} for i in ServiceGalleryImage.objects.filter(id__in=uploaded_images)]
    
    class Meta:
        model = Service
        fields = ["id",
                  "user", 
                  "name", 
                  "price", 
                  "category_get", 
                  "place_get",
                  "category", 
                  "place",  
                  "experience", 
                  "description", 
                  "status", 
                  "vip_date", 
                  "vip_is_active", 
                  "primary_image", 
                  "gallery_images",
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
        
    class Meta:
        model = Service
        fields = '__all__'


class CategoriesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Service_Category
        fields = '__all__'

    
class HomeCategoriesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Service_Category
        fields = ['id', 'name']


class ServiceLikesFromUsersSerializer(serializers.ModelSerializer):
    user = LikeToUserSerializer()

    class Meta:
        model = Like_Service
        fields = ["user", "date_created"]


class LikeToServiceSerializer(serializers.ModelSerializer):
    user = LikeToUserSerializer()
    
    class Meta:
        model = Service
        fields = ('user', 'name', 'primary_image')


class LikesToServiceSerializer(serializers.ModelSerializer):
    service = LikeToServiceSerializer()

    class Meta:
        model = Like_Service
        fields = ["id", "service", "date_created"]