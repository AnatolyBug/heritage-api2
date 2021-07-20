from django.db import models
from .choices import PLACE_TYPES, FRIENDLY_TAGS, PRICE_CATEGORIES
from datetime import datetime, timedelta
from django.contrib.postgres.fields import ArrayField
#from auths.models import User


class Place(models.Model):
    PlaceType = models.TextChoices('PlaceType', PLACE_TYPES)
    FriendlyTag = models.TextChoices('FriendlyTag', FRIENDLY_TAGS)

    external_id = models.UUIDField(db_column="ei", primary_key=True, unique=True, editable=False)
    name = models.CharField(db_column="n", blank=False, max_length=30)
    type = models.CharField(db_column="t", choices=PlaceType.choices, blank=False, max_length=20)
    description = models.TextField(db_column="d", max_length=1000, null=True)
    address = models.JSONField(db_column="a", blank=False)
    images = ArrayField(db_column='ii', null=True, base_field=models.ImageField())
    #geo = models.PointField(db_field="geo", auto_index=False)
    price_category = models.IntegerField(db_column="p", choices=PRICE_CATEGORIES, blank=False)
    created = models.DateTimeField(db_column="c", default=datetime.utcnow, blank=False)
    live = models.BooleanField(db_column="l", default=True, blank=False)
    friendly_tags = ArrayField(db_column="ft", choices=FriendlyTag.choices, default=None,
                               base_field=models.CharField(max_length=20))
    created_by_user = models.ForeignKey('auths.User', blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['live', 'user'])
        ]
