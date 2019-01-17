from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone
# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumMethod:
    def get_read_num(self):
        try:
            blog = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=blog,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
           return 0


class ReadNumDetail(models.Model):
    read_num = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')