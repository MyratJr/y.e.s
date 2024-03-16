import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from advertisement.views import validate_image
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


phone_regex = RegexValidator(
        regex=r"^\+(?:99361|99362|99363|99364|99365|99371)\d{6}$",
        message="Phone number must be entered in the format +99361-->65XXXXXX or +99371XXXXXX, where XXXXXXX is the 7-digit subscriber number."
    )


def validate_image(image):
    max_width = 1024
    max_height = 768
    width, height = get_image_dimensions(image)
    
    if width > max_width or height > max_height:
        raise ValidationError("Image dimensions exceed allowed limits: %(width)sx%(height)s. Maximum allowed: %(max_width)sx%(max_height)s." % {
            'width': width,
            'height': height,
            'max_width': max_width,
            'max_height': max_height,
        })


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to="user/avatar_images", 
                               default="user/avatar_images/8380015.jpg"
    )
    REGISTRATION_CHOICES = {
        'email':'Email',
        'google': 'Google',
    }
    registration_method = models.CharField(
        max_length=6,
        default=REGISTRATION_CHOICES.get("email"),
    )
    banner_image = models.ImageField(upload_to="user/avatar_bg_images", 
                                     validators=[validate_image], 
                                     default="user/avatar_bg_images/18220884_v1016-b-09.jpg"
    )
    experience = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    web = models.URLField(max_length=200, blank=True, null=True)
    tiktok = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    imo = models.CharField(max_length=50, blank=True, null=True)
    fisrt_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=12)
    rate_point = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    rate_point_total = models.IntegerField(default=0)
    point_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }