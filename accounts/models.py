from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    uuid = models.UUIDField(verbose_name='uuid',
                            name='uuid', default=uuid4, editable=False)
    verified_at = models.DateTimeField(
        verbose_name='Verified At', name='verified_at', null=True, blank=True)

    def toJson(self):
        return {
            'username': self.username,
            'id': self.uuid.hex,
            'joined': self.date_joined
        }

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'