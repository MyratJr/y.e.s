from django.db import models
import uuid

class Advertisement(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='advertisements/%Y/%m/', max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    expired_date = models.DateField()

    def __str__(self):
        return self.title