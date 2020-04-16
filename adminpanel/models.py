import uuid
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from ankadescankaya.slug import slug_save


class AdminLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=254)
    application = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    method = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "AdminLogs"
        ordering = ['-createdDate']


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=254, allow_unicode=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Tag"
        ordering = ['-createdDate']


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=254, allow_unicode=True)
    description = models.CharField(max_length=254)
    isActive = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Report"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=Tag)
