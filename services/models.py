from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError


class Service_Category(models.Model):
    name = models.CharField(max_length=35)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', max_length=255)

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='service_user')
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, related_name='service_category')
    place = models.ForeignKey("places.Districts", on_delete=models.CASCADE, related_name='service_district')
    experience = models.IntegerField()
    description = models.TextField(validators=[MaxLengthValidator(250)])
    vip_date = models.DateField(blank=True, null=True)
    vip_is_active = models.BooleanField(default=False)
    primary_image = models.ImageField(upload_to='service/service_images/%Y/%m/', max_length=255)
    view_counter = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0)

    def clean(self):
        if not self.vip_date and self.vip_is_active:
            raise ValidationError('Can not leave "vip_date" field empty while "vip_is_active" field is True.')
        elif not self.vip_is_active and self.vip_date:
            raise ValidationError('Can not save "vip_date" field with selected date while "vip_is_active" field is False.')
        return super().clean()

    def __str__(self):
        return str(self.id)
    

class ServiceGalleryImage(models.Model):
    product = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    image = models.ImageField(upload_to='service/service_gallery_images/%Y/%m/', max_length=255)

    def __str__(self):
        try:
            return f"{self.id}'s gallery images"
        except:
            return "Not related image"