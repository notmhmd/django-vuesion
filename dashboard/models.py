from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=250, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.URLField(null=True, blank=True)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.username
