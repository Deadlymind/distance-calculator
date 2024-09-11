from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        PermissionsMixin

from .managers import UserManager
from countries.models import Countries

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    team = models.CharField(choices=(
        ('sourcing', 'Sourcing'),
        ('sales', 'Sales'),
    ), default='sourcing', max_length=10)

    objects = UserManager()

    countries = models.ManyToManyField(Countries, related_name='users')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.id} | {self.username} | {self.team}"