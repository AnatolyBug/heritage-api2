from django.db import models
from auths.models import User


class Relationships(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE, blank=True)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'relationships'
        unique_together = ('from_user', 'to_user',)
