from django.core.validators import RegexValidator
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


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