from django.db import models
from .choices import PLACE_TYPES, FRIENDLY_TAGS, PRICE_CATEGORIES
from datetime import datetime, timedelta

class Place(models.Model):
    PlaceType = models.TextChoices('PlaceType', PLACE_TYPES)

    external_id = models.CharField(db_column="ei", max_length=20,unique=True, editable=False)
    name = models.CharField(db_column="n", blank=False, max_length=30)
    type = models.CharField(db_column="t", choices=PlaceType.choices, blank=False, max_length=20)
    description = models.TextField(db_column="d", max_length=1000, null=True)
    address = models.JSONField(db_column="a", blank=False)
    images = models.JSONField(db_column='ii', null=True)
    #geo = db.PointField(db_field="geo", auto_index=False)
    price_category = models.IntegerField(db_column="p", choices=PRICE_CATEGORIES, blank=False)
    created = models.DateTimeField(db_column="c", default=datetime.utcnow, blank=False)
    live = models.BooleanField(db_column="l", default=True, blank=False)
    #friendly_tags = models.ArrayField(db_column="ft", choices=FRIENDLY_TAGS, default=None, )
    #user=models.ForeignKey()
