from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email


