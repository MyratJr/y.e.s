from django.db import models
import uuid


class Regions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name} and {self.id}'


class Districts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='region_district')
    district = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.district} and {self.id}'