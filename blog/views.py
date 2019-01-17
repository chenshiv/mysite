from django.shortcuts import render_to_response,get_object_or_404,render
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog,BlogType
from comment.models import Comment
from read_num.utils import tongjimethod
from comment.forms import CommentForm


each_page_blogs_number = 5
def get_blogs_list_common(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, each_page_blogs_number) #每篇进行分页
    page_num = request.GET.get('page', 1) #获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginator.num_pages]#页码范围
    #加上省略号
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')
    #加上首页和末页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates = Blog.objects.dates('created_time','month',order="DESC")
    blog_date_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count

    context = {} 
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_dates'] = blog_date_dict
    context['blogt_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blogs_list_common(request,blogs_all_list)
    return render(request,'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_key = tongjimethod(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    context = {}
    context['comments'] = comments
    context['privious_blog'] = Blog.objects.filter(created_time__gt =blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt =blog.created_time).first()
    context['user'] = request.user
    context['blog'] = blog
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type,'object_id':blog_pk,'reply_comment_id':'0'})
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_key,'true')
    return response


def blogs_with_type(request, blogs_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blogs_list_common(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html', context)

def blog_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blogs_list_common(request,blogs_all_list)
    context['blog_with_day'] = '%s年%s月'%(year,month)
    return render(request,'blog/blog_with_date.html',context)
# Create your views here.
