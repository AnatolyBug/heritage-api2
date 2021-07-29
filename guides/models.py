from django.db import models


class FriendlyTags(models.Model):
    tag_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'friendly_tags'
