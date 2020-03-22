from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='comments')
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    Content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField()

    class Meta:
        ordering = ["-created_time"]
