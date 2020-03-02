import uuid
from ckeditor.fields import RichTextField
from django.db import models
from rest_framework.fields import FileField

from account.models import Account
from adminpanel.models import Tag


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sınav Soruları Id")
    title = models.CharField(max_length=254, verbose_name="Okul Adı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Okul Adı Slug")
    description = RichTextField(verbose_name="Okul Açıklama", null=True,
                                blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Okul Oluşturulma Tarihi")
    updatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)
    since = models.DateTimeField(verbose_name="Okul Kurulduğu Tarih")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Okul Oluşturan Kişi")
    media = models.FileField(null=True, blank=True, verbose_name="Dosya")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "School"
        ordering = ['-createdDate']


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Bölüm Id")
    title = models.CharField(max_length=254, verbose_name="Bölüm Adı")
    slug = models.SlugField(unique=True, max_length=254,
                            verbose_name="Bölüm Adı Slug")
    description = models.TextField(verbose_name="Bölüm Açıklama ", null=True,
                                   blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Bölüm Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Bölüm Güncellendiği Tarih", null=True, blank=True)
    schoolId = models.ForeignKey(School, verbose_name="Okul Adı",
                                 on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Bölüm Oluşturan Kişi")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    media = models.FileField(null=True, blank=True, verbose_name="Dosya")
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Department"
        ordering = ['-createdDate']


class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Dönem Id")
    title = models.CharField(max_length=254, verbose_name="Dönem (Bahar-Kış-Yaz)")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Dönem Slug")
    departmentId = models.ForeignKey(Department, verbose_name="Bölüm", on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Dönem Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Dönem Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Term"
        ordering = ["-createdDate"]


class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sınav Sorusu Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, verbose_name="Sınav Sorusu Oluşturan", null=True)
    title = models.CharField(max_length=254, verbose_name="Sınav Sorusu Başlık")
    description = RichTextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Sınav Sorusu Slug")
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Sınav Sorusu Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Sınav Sorusu Güncellendiği Tarih", null=True, blank=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    termId = models.ForeignKey(Term, on_delete=models.SET_NULL, verbose_name="Dönem", null=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Lecture"
        ordering = ['-createdDate']


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sınav Sorusu Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, verbose_name="Sınav Sorusu Oluşturan", null=True)
    title = models.CharField(max_length=254, verbose_name="Sınav Sorusu Başlık")
    description = RichTextField()
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Sınav Sorusu Slug")
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Sınav Sorusu Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Sınav Sorusu Güncellendiği Tarih", null=True, blank=True)
    media = models.FileField(null=True, blank=True, verbose_name="Dosya")
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    lectureId = models.ForeignKey(Lecture, verbose_name="Ders Adı",
                                  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Exam"
        ordering = ['-createdDate']


class ExamComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Yorum Id")
    examId = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, verbose_name="Makale Yorumcusu")
    creator = models.CharField(max_length=50, verbose_name="Kullanıcı Adı", null=False, blank=False)
    content = RichTextField(verbose_name="Yorum", blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, related_name="Cevap", on_delete=models.SET_NULL)
    isRoot = models.BooleanField(default=False, verbose_name="Root Durumu")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    like = models.PositiveIntegerField(default=0, verbose_name="Yorum Beğeni Sayısı")
    media = models.FileField(default='default-user-image.png', verbose_name="Dosya")

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "ExamComment"
        ordering = ['-createdDate']


class ExamTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Tag Id")
    examId = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, verbose_name="Makale")
    tagId = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Sınav Tag Görüntülenme Tarihi")

    def __str__(self):
        return self.examId

    class Meta:
        db_table = "ExamTag"
