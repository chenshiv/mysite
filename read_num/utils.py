import datetime
from django.contrib.contenttypes.models import ContentType 
from django.utils import timezone
from django.db.models import Sum,Count
from .models import ReadNum,ReadNumDetail  
from blog.models import Blog
  
def tongjimethod(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key =  "%s_%s" %(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        #计数加1
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        readDetail, created = ReadNumDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_date_read_num(content_type):
    read_nums = []
    dates = []
    today = timezone.now().date()
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadNumDetail.objects.filter(content_type=content_type,date=date)
        resutl = read_detail.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(resutl['read_num_sum'] or 0)
    return read_nums,dates


def get_today_hot_date():
    today = timezone.now().date()
    read_detail = Blog.objects.filter(read_details__date=today) \
                                       .values('id','title') \
                                       .annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return read_detail[:7]

def get_yesterday_hot_date():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = Blog.objects.filter(read_details__date=yesterday) \
                                       .values('id','title') \
                                       .annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return read_detail[:7]


def get_seven_day_hot_date(day):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=day)
    read_detail = Blog.objects.filter(read_details__date__lte=today,read_details__date__gte=date) \
                                       .values('id','title') \
                                       .annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
                                       
    return read_detail[:7]