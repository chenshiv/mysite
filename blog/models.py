from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_num.models import ReadNumMethod,ReadNumDetail

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model,ReadNumMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    read_details = GenericRelation(ReadNumDetail)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    lasted_update_time = models.DateTimeField(auto_now=True)

    
    
    
    def __str__(self):
        return "<Blog: %s>" % self.title
    
    class Meta():
        ordering = ['-created_time']


    
# Create your models here.
