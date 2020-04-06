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

    root = models.ForeignKey(
        'self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        'self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(
        User, related_name="replies", null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created_time"]
