import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from account.models import Account


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Kategori Id")
    course_category_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    course_category_title = models.CharField(max_length=254, verbose_name="Kurs Kategori Başlığı")
    course_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Kurs Kategori Slug")
    course_category_description = models.TextField(verbose_name="Kurs Kategori Açıklama", null=True, blank=True)
    course_category_created_date = models.DateTimeField(auto_now_add=True,
                                                        verbose_name="Kurs Kategori Oluşturulduğu Tarih")

    def __str__(self):
        return self.course_category_title

    class Meta:
        ordering = ['-course_category_created_date']


class CourseSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Alt Kategori Id")
    course_sub_category_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    course_sub_category_title = models.CharField(max_length=254, verbose_name="Kurs Alt Kategori Başlığı")
    course_sub_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Kurs Alt Kategori Slug")
    course_sub_category_description = models.TextField(verbose_name="Kurs Alt Kategori Açıklama", null=True,
                                                       blank=True)
    course_sub_category_created_date = models.DateTimeField(auto_now_add=True,
                                                            verbose_name="Kurs Alt Kategori Oluşturulduğu Tarih")
    course_category_id = models.ForeignKey(CourseCategory, verbose_name="Kurs Ana Kategori",
                                           on_delete=models.CASCADE)

    def __str__(self):
        return self.course_sub_category_title

    class Meta:
        ordering = ['-course_sub_category_created_date']


class CourseSubToSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs En Alt Kategori Id")
    course_sub_to_sub_category_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    course_sub_to_sub_category_title = models.CharField(max_length=254, verbose_name="Kurs En Alt Kategori Başlığı")
    course_sub_to_sub_category_slug = models.SlugField(
        unique=True, max_length=254, verbose_name="Kurs En Alt Kategori Slug")
    course_sub_to_sub_category_description = models.TextField(
        verbose_name="Kurs En Alt Kategori Açıklama", null=True, blank=True)
    course_sub_to_sub_category_created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Kurs En Alt Kategori Oluşturulduğu Tarih")
    course_sub_category_id = models.ForeignKey(
        CourseSubCategory, verbose_name="Kurs Alt Kategori", on_delete=models.CASCADE)

    def __str__(self):
        return self.course_sub_to_sub_category_title

    class Meta:
        ordering = ['-course_sub_to_sub_category_created_date']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Id")
    course_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Kurs Öğretmeni")
    course_sub_to_sub_category_id = models.ForeignKey(CourseSubToSubCategory, verbose_name="Kurs En Alt Kategori",
                                               on_delete=models.CASCADE)
    course_title = models.CharField(max_length=254, verbose_name="Kurs Başlığı")
    course_slug = models.SlugField(unique=True, max_length=254, verbose_name="Kurs Slug")
    course_content = RichTextField(verbose_name="Kurs Açıklaması")
    course_media = models.FileField(null=True, blank=True, verbose_name="Kurs Dosya Yükleme")
    course_created_date = models.DateTimeField(auto_now_add=True, verbose_name="Kurs Oluşturulduğu Tarih")
    course_view = models.PositiveIntegerField(default=0, verbose_name="Kurs Görüntülenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.course_title

    class Meta:
        ordering = ['-course_created_date']
