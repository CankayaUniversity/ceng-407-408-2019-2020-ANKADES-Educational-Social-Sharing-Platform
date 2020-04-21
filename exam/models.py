import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import ExamMediaStorage


class ExamCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, allow_unicode=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    isRoot = models.BooleanField(default=False)
    isSchool = models.BooleanField(default=False)
    isDepartment = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "ExamCategory"


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.PositiveIntegerField(default=1)
    lectureCode = models.CharField(null=False, blank=False, max_length=50)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    categoryId = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=254, null=False, blank=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    media = models.FileField(null=True, blank=True, storage=ExamMediaStorage())

    def __str__(self):
        return self.lectureCode

    def __unicode__(self):
        return self.lectureCode

    class Meta:
        db_table = "Exam"


pre_save.connect(slug_save, sender=Exam)