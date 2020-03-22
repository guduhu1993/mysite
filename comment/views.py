from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from django.urls import reverse
# Create your views here.


def update_comment(requests):
    referer = requests.META.get('HTTP_REFERER', reverse='home')
    user = requests.user
    if not user.is_authenticated:
        return render(requests, 'error.html', {"massage": "用户未登录", "referer_to": referer})
    text = requests.POST.get('text', '').strip()
    if text == '':
        return render(requests, 'error.html', {"massage": "没有内容", "referer_to": referer})
    object_id = int(requests.POST.get("object_id", ""))
    content_type = requests.POST.get("content_type", "")
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(id=object_id)

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.Content_object = model_obj
    comment.save()

    return redirect(referer)
