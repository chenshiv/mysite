from django.shortcuts import render_to_response,render,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from read_num.utils import get_date_read_num,get_today_hot_date,get_yesterday_hot_date,get_seven_day_hot_date
from blog.models import Blog
from django.core.cache import cache
from django.urls import reverse
from .forms import LoginForm,RegForm


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums,dates = get_date_read_num(blog_content_type)
    #获取七天缓存
    seven_day_hot_date = cache.get('seven_day_hot_date')
    if seven_day_hot_date is None:
        seven_day_hot_date = get_seven_day_hot_date(7)
        cache.set('seven_day_hot_date',seven_day_hot_date,600)
    month_day_hot_date = get_seven_day_hot_date(30)
    context={}
    context['hot_date'] = get_today_hot_date()
    context['yesterday_hot_date'] = get_yesterday_hot_date()
    context['seven_day_hot_date'] = seven_day_hot_date
    context['month_day_hot_date'] = month_day_hot_date
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render(request,'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def logout(request):
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    auth.logout(request)
    return redirect(referer)