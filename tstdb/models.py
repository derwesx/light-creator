from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=128, default='conf', unique=True)
    value = models.CharField(max_length=131072, default='val')
