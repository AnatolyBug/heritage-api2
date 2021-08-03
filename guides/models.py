from django.db import models
from auths.models import User
from places.models import Places
from django.contrib.postgres.fields import ArrayField


class FriendlyTags(models.Model):
    tag_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'friendly_tags'


class TransportMethods(models.Model):
    transport_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'transport_methods'


class Guides(models.Model):
    place = models.ManyToManyField(Places, related_name='place', blank=True, null=True)
    main_transport_method = models.ForeignKey(
        TransportMethods, related_name='main_transport_method', on_delete=models.CASCADE, blank=True, null=True)
    friendly_tag = models.ForeignKey(
        FriendlyTags, related_name='friendly_tag', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name='guide_user', on_delete=models.CASCADE, blank=True, null=True)
    duration = models.IntegerField(blank=True)
    transport_methods = ArrayField(models.CharField(max_length=50, blank=True), null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'guides'
