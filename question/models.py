import uuid
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from account.models import Account
from adminpanel.models import Tag


class QuestionCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Kategori Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Oluşturan Kişi")
    title = models.CharField(max_length=254, verbose_name="Makale Kategori Başlığı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Makale Kategori Slug")
    description = models.TextField(verbose_name="Makale Kategori Açıklama", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Makale Kategori Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Makale Kategori Güncellendiği Tarih", null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, verbose_name="Üst Kategorisi")
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
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Makale Öğretmeni")
    categoryId = models.ForeignKey(QuestionCategory, verbose_name="Makale Kategori",
                                   on_delete=models.SET_NULL, null=True)
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


class QuestionComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Yorum Id")
    questionId = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name="Makale Yorumcusu")
    creator = models.CharField(max_length=50, verbose_name="Kullanıcı Adı", null=False, blank=False)
    content = RichTextField(verbose_name="Yorum", blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, related_name="Cevap", on_delete=models.SET_NULL)
    isRoot = models.BooleanField(default=False, verbose_name="Root Durumu")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    view = models.PositiveIntegerField(default=0, verbose_name="Yorum Görüntülenme Tarihi")
    like = models.PositiveIntegerField(default=0, verbose_name="Yorum Beğeni Sayısı")

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "QuestionComment"
        ordering = ['-createdDate']


class QuestionTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Tag Id")
    questionId = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name="Makale")
    tagId = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.questionId

    class Meta:
        db_table = "QuestionTag"