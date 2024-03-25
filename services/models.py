from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid


class Service_Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=35, verbose_name = 'Ady')
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', max_length=255, verbose_name="Suraty")

    class Meta:
        verbose_name_plural = 'Hyzmat kategoriýalary'

    def __str__(self):
        return f'{self.name} and {self.id}'


class ServiceVerification(models.TextChoices):
    Kabul_Edildi = "Siziň hyzmatyňyz kabul edildi."
    Garashylyar = "Häzirki wagtda siziň goýan hyzmatyňyz barlanylýar, biraz garaşmagyňyzy haýyş edýäris."
    Showsyz = """Bagyşlaň, siziň goýan hyzmatyňyz 'Hyzmat goýluş düzgünleri'-e laýyl gelmeýär.
                Hyzmat üçin gerekli maglumatlary talaba laýyk dolduryň we täzeden synanyşyň."""


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='service_user', verbose_name = 'Ulanyjy')
    name = models.CharField(max_length=25, verbose_name = 'Ady')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name = 'Bahasy')
    category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, related_name='service_category', verbose_name = 'Kategoriýasy')
    place = models.ForeignKey("places.Districts", on_delete=models.CASCADE, related_name='service_district', verbose_name = 'Ýerleşýän ýeri')
    experience = models.IntegerField(verbose_name = 'Tejribäňiz (ýylda)')
    description = models.TextField(validators=[MaxLengthValidator(250)], verbose_name = 'Barada')
    status = models.CharField(max_length=500, choices=ServiceVerification.choices, default=ServiceVerification.Garashylyar, verbose_name = 'Ýagdaý')
    vip_date = models.DateField(blank=True, null=True, verbose_name = 'V.I.P gutarýan senesi')
    vip_is_active = models.BooleanField(default=False, verbose_name = 'V.I.P ýagdaýy')
    primary_image = models.ImageField(upload_to='service/service_images/%Y/%m/', max_length=255, verbose_name='Suraty')
    view_counter = models.IntegerField(default=0, verbose_name = 'Görülenleri sanaýjy')
    like_counter = models.IntegerField(default=0, verbose_name = 'Halanlary sanaýjy')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name = 'Goýlan senesi')

    class Meta:
        verbose_name_plural = 'Hyzmatlar'

    def clean(self):
        if not self.vip_date and self.vip_is_active:
            raise ValidationError('"V.I.P ýagdaýy" açyk wagty "V.I.P gutarýan senesi"-ni boş goýup bolmaýar. "V.I.P gutarýan senesi"-ne sene giriziň.')
        elif not self.vip_is_active and self.vip_date:
            raise ValidationError('"V.I.P ýagdaýy" ýapyk wagty "V.I.P gutarýan senesi"-ne sene girizip bolmaýar. "V.I.P gutarýan senesi"-ne girizen senäňizi aýyryň.')
        return super().clean()

    def __str__(self):
        return f'{self.name} and {self.id}'


class ServiceGalleryImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="images", verbose_name = 'Hyzmat')
    image = models.ImageField(upload_to='service/service_gallery_images/%Y/%m/', max_length=255, verbose_name="Suraty")

    class Meta:
        verbose_name_plural = 'Hyzmatyň galereýasy'

    def __str__(self):
        try:
            return f"{self.product} and {self.id}'s gallery images"
        except:
            return "Not related image"