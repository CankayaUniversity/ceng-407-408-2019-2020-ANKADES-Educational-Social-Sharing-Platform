import uuid
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Kategori Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Oluşturan Kişi")
    title = models.CharField(max_length=254, verbose_name="Kurs Kategori Başlığı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Slug", allow_unicode=True)
    description = RichTextField(verbose_name="Kurs Kategori Açıklama", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Kurs Kategori Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Kurs Kategori Güncellendiği Tarih", null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, verbose_name="Üst Kategorisi")
    isRoot = models.BooleanField(default=False, verbose_name="Root Durumu")
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0, verbose_name="Makale Görüntülenme Tarihi")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseCategory"
        ordering = ['-createdDate']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Id")
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Kurs Öğretmeni")
    categoryId = models.ForeignKey(CourseCategory, verbose_name="Kurs Kategori",
                                   on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, verbose_name="Kurs Başlığı")
    slug = models.SlugField(unique=True, max_length=254, verbose_name="Slug", allow_unicode=True)
    description = RichTextField(verbose_name="Kurs Açıklaması")
    media = models.FileField(null=True, blank=True, verbose_name="Kurs Dosya Yükleme")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Kurs Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Kurs Güncellendiği Tarih", null=True, blank=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Kurs Görüntülenme Tarihi")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    isPrivate = models.BooleanField(default=False, verbose_name="Kurs Özel Mi ?")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Course"
        ordering = ['-createdDate']


class CourseSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Bölüm Id")
    title = models.CharField(max_length=254, verbose_name="Kurs Başlığı")
    description = RichTextField(verbose_name="Section Açıklaması")
    updatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Kurs Bölüm Düzenlendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    view = models.PositiveIntegerField(default=0, verbose_name="Makale Görüntülenme Tarihi")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Bölüm Oluşturulduğu Tarih")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseSection"


class CourseLecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Ders Id")
    title = models.CharField(max_length=254, verbose_name="Ders Başlığı")
    description = RichTextField(verbose_name="Ders Açıklaması")
    sectionId = models.ForeignKey(CourseSection, on_delete=models.SET_NULL, null=True, verbose_name="Bölüm Adı")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Ders Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Ders Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")
    media = models.FileField(verbose_name="Dosya")
    isQuiz = models.BooleanField(default=False, verbose_name="Quiz mi?")
    question = RichTextField(verbose_name="Quiz Sorusu")
    answer = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0, verbose_name="Makale Görüntülenme Tarihi")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseLecture"


class CourseComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Yorum Id")
    courseId = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Makale Yorumcusu")
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
        db_table = "CourseComment"
        ordering = ['-createdDate']


class CourseTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Tag Id")
    tagId = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, verbose_name="Etiket")
    courseId = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Kurs")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0, verbose_name="Yorum Görüntülenme Tarihi")
    like = models.PositiveIntegerField(default=0, verbose_name="Yorum Beğeni Sayısı")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.tagId

    class Meta:
        db_table = "CourseTag"


pre_save.connect(slug_save, sender=CourseCategory)
pre_save.connect(slug_save, sender=Course)
pre_save.connect(slug_save, sender=CourseSection)
pre_save.connect(slug_save, sender=CourseLecture)