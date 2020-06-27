from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.Content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    # print(data)
    return JsonResponse(data)
