from django.db import models
from auths.models import User
from guides.models import Guides


class Comments(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', blank=True)
    comment_guide = models.ForeignKey(Guides, on_delete=models.CASCADE, related_name='comment_guide', blank=True)
    comment = models.TextField(blank=True)
    like = models.BooleanField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'comments'
