from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.


def update_comment(request):
    '''referer = request.META.get('HTTP_REFERER')
    user = request.user
    if not user.is_authenticated:
        return render(request, 'error.html', {"massage": "用户未登录", "referer_to": referer})
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {"massage": "没有内容", "referer_to": referer})
    object_id = int(request.POST.get("object_id", ""))
    print()
    content_type = request.POST.get("content_type", "")
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(id=object_id)

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.Content_object = model_obj
    comment.save()

    return redirect(referer)'''

    # referer = request.META.get('HTTP_REFERER')
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
        # data['username']=comment.user.username
        # data['comment_time']=comment.cre  ated_time.strftime('%Y-%m-%D %H-%M-%S')
        # data['text']=comment.text
    else:
        data['status'] = 'ERROR'
    # print(data)
    return JsonResponse(data)
