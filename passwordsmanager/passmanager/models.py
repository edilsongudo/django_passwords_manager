from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Entry(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100, default='')
    site_email_used = models.EmailField(max_length=100, blank=True, default='')
    site_password_used = models.CharField(max_length=100, default='')
    is_generated_for_initial_master_pw_check = models.BooleanField(
        default=False)

    def __str__(self):
        return f'{self.author.username} Entry {self.pk}'


class MasterPassword(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.CASCADE)
    has_defined_a_master_password = models.BooleanField(
        default=False)

    def __str__(self):
        return f'{self.author.username} hashed Master Password'
