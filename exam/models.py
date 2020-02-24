import uuid
from ckeditor.fields import RichTextField
from django.db import models
from rest_framework.fields import FileField
from account.models import Account


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sınav Soruları Id")
    schoolTitle = models.CharField(max_length=254, verbose_name="Okul Adı")
    schoolSlug = models.SlugField(unique=True, max_length=254, verbose_name="Okul Adı Slug")
    schoolDescription = RichTextField(verbose_name="Okul Açıklama", null=True,
                                      blank=True)
    schoolCreatedDate = models.DateTimeField(auto_now_add=True,
                                             verbose_name="Okul Oluşturulma Tarihi")
    schoolUpdatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)
    schoolSince = models.DateTimeField(verbose_name="Okul Kurulduğu Tarih")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Okul Oluşturan Kişi")
    schoolImage = FileField(default='default-user-image.png')
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.schoolTitle

    class Meta:
        db_table = "School"
        ordering = ['-schoolCreatedDate']


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Bölüm Id")
    title = models.CharField(max_length=254, verbose_name="Bölüm Adı")
    slug = models.SlugField(unique=True, max_length=254,
                            verbose_name="Bölüm Adı Slug")
    departmentDescription = models.TextField(verbose_name="Bölüm Açıklama ", null=True,
                                             blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Bölüm Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Bölüm Güncellendiği Tarih", null=True, blank=True)
    schoolId = models.ForeignKey(School, verbose_name="Okul Adı",
                                 on_delete=models.CASCADE)
    image = FileField(default='default-user-image.png')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Bölüm Oluşturan Kişi")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Department"
        ordering = ['-createdDate']


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sınav Sorusu Id")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Sınav Sorusu Oluşturan")
    title = models.CharField(max_length=254, verbose_name="Sınav Sorusu Başlık")
    description = RichTextField()
    examSlug = models.SlugField(unique=True, max_length=254, verbose_name="Sınav Sorusu Slug")
    createdDate = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Sınav Sorusu Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Sınav Sorusu Güncellendiği Tarih", null=True, blank=True)
    departmentId = models.ForeignKey(Department, verbose_name="Bölüm Adı",
                                     on_delete=models.CASCADE)
    media = models.FileField(default='default-user-image.png', verbose_name="Dosya")
    view = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Exam"
        ordering = ['-createdDate']
