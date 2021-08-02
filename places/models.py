from django.db import models
from auths.models import User
from django.contrib.postgres.fields import ArrayField


class PlaceTypes(models.Model):
    place_type = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'place_types'


class PriceCategories(models.Model):
    category_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'price_categories'


class Places(models.Model):
    place_type = models.ForeignKey(
        PlaceTypes, related_name='price_type', on_delete=models.CASCADE, blank=True, null=True)
    price_category = models.ForeignKey(
        PriceCategories, related_name='price_category', on_delete=models.CASCADE, blank=True, null=True)
    created_by_user = models.ForeignKey(
        'auths.User', related_name='user', blank=False, null=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(null=True)
    address = models.CharField(max_length=255, blank=True)
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)
    images = ArrayField(models.URLField(blank=True), null=True)
    audio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    live = models.BooleanField(default=True, blank=False)

    class Meta:
        db_table = 'places'
