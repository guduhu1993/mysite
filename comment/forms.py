from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea,
                           error_messages={'required': '评论内容不能为空'})
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))
    print(reply_comment_id)
    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(
                model=content_type).model_class()
            model_obj = model_class.objects.get(id=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论文章不存在')
        print(11111)
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(id=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(
                id=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        print(22222222222)
        return reply_comment_id
