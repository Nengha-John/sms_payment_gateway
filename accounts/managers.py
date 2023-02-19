from django.contrib.auth.base_user import BaseUserManager
import uuid


class CustomUserManager(BaseUserManager):

    def create_user(self, **kwargs):
        user = self.model(**kwargs)
        password = kwargs.get('password')
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff to True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser to True')
        user = self.create_user(**kwargs)
        return user

