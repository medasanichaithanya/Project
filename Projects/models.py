from django.db import models

# Create your models here.
class Information(models.Model):
    height = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    age = models.FloatField(null=True,blank=True)
    waist = models.FloatField(null=True,blank=True)
