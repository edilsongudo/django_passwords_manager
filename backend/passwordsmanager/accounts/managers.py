from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Overriding BaseUserManager in order to allow users to register and authenticate by using email instead of username.
    """

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email field is required')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)
