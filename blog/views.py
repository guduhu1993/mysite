from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Blog, BlogType
from django.core.paginator import Paginator
import markdown
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from mysite.views import parse_payload
from mysite.views import login_required

# Create your views here.

@login_required
def blog_list(requests):
    # jwt_token=requests.COOKIES.get('jwt_token')
    # result=parse_payload(jwt_token)
    # print(jwt_token)
    # if result['error']:
    #     context['massage'] = result['error']
    #     context['referer_to'] = 'login'
    #     return redirect('login')
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
            i for i in range(int(contacts.number) - 2, int(contacts.number) + 3)]
    elif int(contacts.number) in [1, 2]:
        context['current_page_list'] = range(1, len(paginator.page_range)+1)
    elif int(contacts.number) > len(paginator.page_range) - 2:
        context['current_page_list'] = range(
            all_page_num - 4, all_page_num + 1)
    context['types'] = get_list_or_404(BlogType)
    context['next_page'] = contacts.next_page_number(
    ) if contacts.has_next() else contacts.number
    context['previous_page'] = contacts.previous_page_number(
    ) if contacts.has_previous() else contacts.number
    return render(requests, 'blog/blogs_list.html', context)

@login_required
def blog_detail(requests,blog_id):
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

@login_required
def blog_type(requests, blog_type_id):
    context = {}
    blog_type_list = get_list_or_404(Blog, blog_type = blog_type_id)
    paginator = Paginator(blog_type_list, 10)
    current_type_page = requests.GET.get('page') if requests.GET.get('page') else 1
    # print("------",current_type_page)
    contacts = paginator.get_page(current_type_page)
    all_page_num = len(paginator.page_range)
    # print("======", type(contacts.number))
    context['all_page_num'] = all_page_num
    if all_page_num - 1 > contacts.number > 2:
        context['current_page_list'] = [i for i in range(contacts.number - 2, contacts.number + 3)]
    elif contacts.number in [1, 2]:
        context['current_page_list'] = range(1, all_page_num + 1 if all_page_num <= 5 else  5)
    elif contacts.number > len(paginator.page_range) - 2:
        context['current_page_list'] = range(all_page_num - 4, all_page_num + 1)
    context['types'] = get_list_or_404(BlogType)
    context['next_page'] = contacts.next_page_number() if contacts.has_next() else contacts.number
    context['previous_page'] = contacts.previous_page_number() if contacts.has_previous() else contacts.number
    # context['blogs'] = Blog.objects.filter('blog_type')
    context['blogs'] = contacts
    context['all_blogs_number'] = blog_type_list
    return render(requests, 'blog/blog_with_type.html', context)

@login_required
def search(requests):
    context = {}
    search_wd = requests.GET.get('wd')
    blogs_page_list = Blog.objects.filter(content__icontains=search_wd)
    paginator = Paginator(blogs_page_list, 10)
    page_num = requests.GET.get('page')
    contacts = paginator.get_page(page_num)
    all_page_num = len(paginator.page_range)
    context['search_wd'] = search_wd
    context['blogs'] = blogs_page_list
    context['page_result'] = contacts
    context['all_page_num'] = all_page_num
    if len(paginator.page_range) - 1 > int(contacts.number) > 2:
        context['current_page_list'] = [
            i for i in range(int(contacts.number) - 2, int(contacts.number) + 3)]
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
    return render(requests, 'blog/search/search.html', context)

@login_required
def query(request):
    return render(request,'blog/query.html')