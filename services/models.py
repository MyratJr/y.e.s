from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid


class Service_Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=35)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', max_length=255)

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='service_user', null=True)
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, related_name='service_category')
    place = models.ForeignKey("places.Districts", on_delete=models.CASCADE, related_name='service_district')
    experience = models.IntegerField()
    description = models.TextField(validators=[MaxLengthValidator(250)])
    public = models.BooleanField(default=False)
    vip_date = models.DateField(blank=True, null=True)
    vip_is_active = models.BooleanField(default=False)
    primary_image = models.ImageField(upload_to='service/service_images/%Y/%m/', max_length=255)
    view_counter = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    def clean(self):
        if not self.vip_date and self.vip_is_active:
            raise ValidationError('Can not leave "vip_date" field empty while "vip_is_active" field is True.')
        elif not self.vip_is_active and self.vip_date:
            raise ValidationError('Can not save "vip_date" field with selected date while "vip_is_active" field is False.')
        return super().clean()

    def __str__(self):
        return f'{self.name} and {self.id}'
    
    def __init__(self, *args, **kwargs):
        self.is_new=False
        self.save()
    

class ServiceGalleryImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    image = models.ImageField(upload_to='service/service_gallery_images/%Y/%m/', max_length=255)

    def __str__(self):
        try:
            return f"{self.product} and {self.id}'s gallery images"
        except:
            return "Not related image"