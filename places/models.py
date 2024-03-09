from django.db import models


class Regions(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Districts(models.Model):
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='region_district')
    district = models.CharField(max_length=50)

    def __str__(self):
        return self.district