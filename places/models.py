from django.db import models
from datetime import datetime, timedelta
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


class Place(models.Model):
    place_type = models.ForeignKey(
        PlaceTypes, related_name='price_type', on_delete=models.CASCADE, blank=True, null=True)
    price_category = models.ForeignKey(
        PriceCategories, related_name='price_category', on_delete=models.CASCADE, blank=True, null=True)

    external_id = models.UUIDField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(null=True)
    address = models.JSONField(blank=True)
    images = ArrayField(null=True, base_field=models.ImageField())
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    live = models.BooleanField(default=True, blank=False)
    created_by_user = models.ForeignKey('auths.User', blank=False, null=True, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['live'])
        ]
        db_table = 'places'
