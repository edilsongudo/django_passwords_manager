from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    # def save(self, *args, **kwargs):
    #     self.username = self.username.lower()
    #     super(User, self).save(*args, **kwargs)
