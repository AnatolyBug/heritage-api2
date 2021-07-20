from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from places.models import Place
# from guides.models import Guide


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    email_confirmed = models.BooleanField(default=False)
    email_verification_id = models.CharField(max_length=30, blank=True)
    saved_places = ArrayField(
        models.ForeignKey(Place, related_name='place', on_delete=models.CASCADE),
        blank=True,
        null=True
    )

    # No Guide models yet
    saved_guides = ArrayField(
        models.ForeignKey(Place, related_name='guide', on_delete=models.CASCADE),
        blank=True,
        null=True
    )
    profile_image = models.ImageField(upload_to='avatar', blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'users'
