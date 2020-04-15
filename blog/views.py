from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
import markdown
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
# Create your views here.


def blog_list(requests):
    context = {}
    blogs_page_list = get_list_or_404(Blog)
    paginator = Paginator(blogs_page_list, 10)
    page_num = requests.GET.get('page')
    contacts = paginator.get_page(page_num)
    all_page_num = len(paginator.page_range)
    context['blogs'] = blogs_page_list
    context['page_blogs'] = contacts
    context['all_page_num'] = all_page_num
    if len(paginator.page_range) - 1 > int(contacts.number) > 2:
        context['current_page_list'] = [
            i for i in range(1, int(contacts.number) + 3)]
    elif int(contacts.number) in [1, 2]:
        context['current_page_list'] = range(1, all_page_num + 1)
    elif int(contacts.number) > len(paginator.page_range) - 2:
        context['current_page_list'] = range(
            all_page_num - 4, all_page_num + 1)
    context['types'] = get_list_or_404(BlogType)
    context['next_page'] = contacts.next_page_number(
    ) if contacts.has_next() else contacts.number
    context['previous_page'] = contacts.previous_page_number(
    ) if contacts.has_previous() else contacts.number
    return render(requests, 'blog/blogs_list.html', context)


def blog_detail(requests, blog_id):
    context = {}
    blog = get_object_or_404(Blog, id=blog_id)
    context['blog'] = blog
    blog_comment_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(
        content_type=blog_comment_type, object_id=blog_id, parent=None)
    context['blog_content'] = markdown.markdown(blog.content.replace("\r\n", '  \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ], safe_mode=True, enable_attributes=False)
    context['types'] = get_list_or_404(BlogType)
    context['previous_blog'] = Blog.objects.filter(
        created_time__gt=blog.created_time).first()
    context['next_blog'] = Blog.objects.filter(
        created_time__lt=blog.created_time).last()
    context['comments'] = comments

    data = {}
    data['content_type'] = blog_comment_type.model
    data['object_id'] = blog_id
    data['reply_comment_id'] = 0
    context['comments_form'] = CommentForm(initial=data)
    return render(requests, 'blog/blog_detail.html', context)


def blog_type(requests, blog_type_id):
    context = {}
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    context['types'] = get_list_or_404(BlogType)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    return render(requests, 'blog/blog_with_type.html', context)
