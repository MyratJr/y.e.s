from django.db import models
from django.utils import timezone
import uuid


class Like_Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Hyzmaty halanlar'


class View_Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Hyzmaty görenler'


class Like_User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    favoriting_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favoriting_user")
    favorited_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favorited_user")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ulanyjyny halanlar'


class View_User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    viewing_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="viewing_user")
    viewed_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="viewed_user")

    class Meta:
        verbose_name_plural = 'Ulanyjyny görenler'


class Rate_User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rating_user")
    rated_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rated_user")
    rate_number = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='rate/%Y/%m/', max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Ulanyja berlen bahalar'

    def __str__(self):
        return f'{self.rating_user} rated {self.rated_user} with {self.rate_number} star.'