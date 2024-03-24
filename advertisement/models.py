from django.db import models
import uuid


class AdvertisementChoises(models.TextChoices):
    Kabul_Edildi = "Siziň mahabatyňyz kabul edildi."
    Mohleti_Gutardy = "Siziň mahabatyňyzyň möhleti gutardy."
    Garashylyar = "Häzirki wagtda siziň goýan mahabatyňyz barlanylýar, biraz garaşmagyňyzy haýyş edýäris."
    Showsyz = """Bagyşlaň, siziň goýan mahabatyňyz 'Mahabat goýluş düzgünleri'-e laýyl gelmeýär.
                Mahabat üçin gerekli maglumatlary talaba laýyk dolduryň we täzeden synanyşyň."""


class Advertisement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20, verbose_name = 'Mahabat ady')
    image = models.ImageField(upload_to='advertisements/%Y/%m/', max_length=255, blank=True, verbose_name = 'Mahabat suraty')
    status = models.CharField(max_length=500, choices=AdvertisementChoises.choices, default=AdvertisementChoises.Garashylyar, verbose_name = 'Ýagdaý')
    expired_date = models.DateField(verbose_name = 'Gutarýan möhleti')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name = 'Goýlan wagty')

    def __str__(self):
        return f'{self.title} and {self.id}'
    
    class Meta:
        verbose_name = 'Mahabat'
        verbose_name_plural = 'Mahabatlar'