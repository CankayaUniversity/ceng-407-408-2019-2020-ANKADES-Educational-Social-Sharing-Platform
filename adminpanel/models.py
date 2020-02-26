import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group, Permission
from django.db import models

from account.models import Account


class AdminActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Id")
    activityCreator = models.CharField(max_length=254, verbose_name="Oluşturan Kişi")
    activityTitle = models.CharField(max_length=254, verbose_name="Başlık")
    activityApplication = models.CharField(max_length=254, verbose_name="Uygulama")
    activityDescription = models.CharField(max_length=254, verbose_name="Açıklama")
    activityMethod = models.CharField(max_length=254, verbose_name="Method Türü")
    activityCreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    activityUpdatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)

    def __str__(self):
        return self.activityCreator

    class Meta:
        db_table = "AdminActivity"
        ordering = ['-activityCreatedDate']