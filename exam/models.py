import uuid
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    isRoot = models.BooleanField(default=False)
    isSchool = models.BooleanField(default=False)
    isDepartment = models.BooleanField(default=False)
    isLecture = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "School"
        ordering = ['-createdDate']


class AccountSchool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)
    schoolId = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        db_table = "AccountSchool"


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lectureId = models.ForeignKey(School, verbose_name="Dersi", on_delete=models.CASCADE)
    term = models.CharField(null=True, blank=True, max_length=32)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    media = models.FileField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Exam"
        ordering = ['-createdDate']


class ExamComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examId = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.PROTECT, null=True, blank=True)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE)
    isRoot = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    media = models.FileField(default='default-user-image.png')

    def __str__(self):
        return self.content

    class Meta:
        db_table = "ExamComment"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=School)
pre_save.connect(slug_save, sender=Exam)
