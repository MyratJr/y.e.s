from django.db import models
from users.models import phone_regex


class SMSStatuses:
    PENDING = "pending"
    DELIVERED = "delivered"
    ACTIVATED = "activated"
    FAILED = "failed"
    VERIFIED = "verified"


class Otp(models.Model):
    phone = models.CharField(validators=[phone_regex], max_length=12)
    status = models.CharField(max_length=20, default=SMSStatuses.PENDING)
    message = models.CharField(max_length=255, blank=True, null=True)
    all_counter = models.IntegerField(default=0)
    each_counter = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'OTP'

    def __str__(self):
        return self.phone
    
    def tried(self):
        self.all_counter+=1
        self.each_counter+=1

        if self.all_counter >=2:
            self.status=SMSStatuses.FAILED
            self.save()