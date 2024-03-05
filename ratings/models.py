from django.db import models
from django.utils import timezone


class Like_Service(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)


class View_Service(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)


class Like_User(models.Model):
    favoriting_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favoriting_user")
    favorited_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favorited_user")
    date_created = models.DateTimeField(default=timezone.now)

class View_User(models.Model):
    viewing_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="viewing_user")
    viewed_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="viewed_user")

class Rate_User(models.Model):
    rating_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rating_user")
    rated_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rated_user")
    rate_number = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='rate/%Y/%m/', max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.rating_user} rated {self.rated_user} with {self.rate_number} star.'