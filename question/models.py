import uuid
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from account.models import Account


class QuestionCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Kategori Id")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    title = models.CharField(max_length=254, verbose_name="Makale Kategori Başlığı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Makale Kategori Slug")
    description = models.TextField(verbose_name="Makale Kategori Açıklama", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Makale Kategori Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Makale Kategori Güncellendiği Tarih", null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Üst Kategorisi")
    isRoot = models.BooleanField(default=False, verbose_name="Root Durumu")
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "QuestionCategory"
        ordering = ['-createdDate']


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Id")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Makale Öğretmeni")
    categoryId = models.ForeignKey(QuestionCategory, verbose_name="Makale Kategori",
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=254, verbose_name="Makale Başlığı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Makale Slug")
    description = RichTextField(verbose_name="Makale Açıklaması")
    media = models.FileField(null=True, blank=True, verbose_name="Makale Dosya Yükleme")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Makale Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Makale Güncellendiği Tarih", null=True, blank=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Makale Görüntülenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Question"
        ordering = ['-createdDate']
