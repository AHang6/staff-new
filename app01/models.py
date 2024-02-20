from django.db import models


# Create your models here.

class Depart(models.Model):
    title = models.CharField(max_length=32)
