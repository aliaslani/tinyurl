from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    origin = models.CharField(max_length=256,unique=True)
    shorted = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.origin} --> {self.shorted}'





