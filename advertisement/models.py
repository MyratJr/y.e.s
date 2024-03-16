from django.db import models
import uuid


class Advertisement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='advertisements/%Y/%m/', max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    expired_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} and {self.id}'