import os

from django.contrib.auth import get_user_model
from django.db import models


class Entry(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100, default='')
    site_email_used = models.EmailField(max_length=100, blank=True, default='')
    site_password_used = models.CharField(max_length=100, default='')
    is_generated_for_initial_master_pw_check = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'{self.author.username} {self.site_name}'


class MasterPassword(models.Model):
    author = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    salt = models.BinaryField(default=os.urandom(32))
    has_defined_a_master_password = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.username}'
