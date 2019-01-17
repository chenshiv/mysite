from django.contrib import admin
from .models import Blog, BlogType


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'blog_type', 'author','get_read_num', 'created_time', 'lasted_update_time')




# Register your models here.

