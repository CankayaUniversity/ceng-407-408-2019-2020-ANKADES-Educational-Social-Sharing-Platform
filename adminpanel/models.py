import uuid
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import pre_save
from account.models import Account
from ankadescankaya.slug import slug_save


class AdminActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    slug = models.SlugField(unique=True, verbose_name="Slug", allow_unicode=True)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.SET_NULL, verbose_name="Kullanıcı Adı", null=True, blank=True)
    title = models.CharField(max_length=254, verbose_name="Başlık")
    application = models.CharField(max_length=254, verbose_name="Uygulama")
    description = models.CharField(max_length=254, verbose_name="Açıklama")
    method = models.CharField(max_length=254, verbose_name="Method Türü")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "AdminActivity"
        ordering = ['-createdDate']


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Tag Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Kullanıcı Adı")
    title = models.CharField(max_length=254, verbose_name="Tag Adı", unique=True)
    slug = models.SlugField(max_length=254, verbose_name="Slug", allow_unicode=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Tag Görüntülenme")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Tag"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=Tag)
pre_save.connect(slug_save, sender=AdminActivity)