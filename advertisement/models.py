from django.db import models
import uuid


class Advertisement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20, verbose_name = 'Mahabat ady')
    image = models.ImageField(upload_to='advertisements/%Y/%m/', max_length=255, blank=True, verbose_name = 'Mahabat suraty')
    is_active = models.BooleanField(default=True, verbose_name = 'Aktiw')
    expired_date = models.DateField(verbose_name = 'Gutarýan möhleti')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name = 'Goýlan wagty')

    def __str__(self):
        return f'{self.title} and {self.id}'