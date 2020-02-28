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


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Tag Id")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    title = models.CharField(max_length=254, verbose_name="Tag Adı", unique=True)
    slug = models.SlugField(max_length=254, verbose_name="Slug")
    view = models.PositiveIntegerField(default=0, verbose_name="Tag Görüntülenme")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Tag"
        ordering = ['-createdDate']