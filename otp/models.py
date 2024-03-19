from django.db import models
from users.models import phone_regex


class SMSStatuses:
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    ACTIVATED = "activated"
    FAILED = "failed"


class Otp(models.Model):
    phone = models.CharField(validators=[phone_regex], max_length=12)
    status = models.CharField(max_length=20, default=SMSStatuses.PENDING)
    message = models.CharField(max_length=255)
    counter = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
    
    def tried(self):
        self.counter+=1

        if self.counter >=3:
            self.status=SMSStatuses.FAILED
            self.save()