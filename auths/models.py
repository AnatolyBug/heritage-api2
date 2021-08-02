from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.core.validators import RegexValidator


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    user_role = models.CharField(max_length=10, default='customer')
    email_confirmed = models.BooleanField(default=False)
    email_verification_id = models.CharField(max_length=30, blank=True)
    saved_places = models.ManyToManyField('places.Places', related_name='place')

    # No Guide models yet
    # saved_guides = models.ManyToManyField(Place, related_name='guide')
    avatar_url = models.URLField(default='default_avatar.png', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'users'
