import uuid

from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import SupportMediaStorage


class SupportSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    isRoot = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "SupportSubject"
        ordering = ['-createdDate']


class Support(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    displayMessage = models.CharField(max_length=255, blank=True, null=True)
    supportNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    postNumber = models.CharField(null=False, blank=False, max_length=32, verbose_name="Application Post Number")
    description = models.CharField(max_length=254)
    isActive = models.BooleanField(default=True)
    isRead = models.BooleanField(default=True)
    isSolved = models.BooleanField(default=True)
    subjectId = models.ForeignKey(SupportSubject, on_delete=models.SET_NULL, null=True, blank=True, related_name="subjectId")
    ownerId = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="ownerId")
    creatorId = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="creatorId")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now_add=True)
    media = models.FileField(null=True, blank=True, storage=SupportMediaStorage())

    def __str__(self):
        return self.supportNumber

    class Meta:
        db_table = "Support"
        ordering = ['-createdDate']


class ReportSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    isRoot = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "ReportSubject"
        ordering = ['-createdDate']


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    displayMessage = models.CharField(max_length=255, blank=True, null=True)
    reportNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    postNumber = models.CharField(null=False, blank=False, max_length=32, verbose_name="Application Post Number")
    description = models.CharField(max_length=254)
    isActive = models.BooleanField(default=True)
    isRead = models.BooleanField(default=True)
    isSolved = models.BooleanField(default=True)
    subjectId = models.ForeignKey(ReportSubject, on_delete=models.SET_NULL, null=True, blank=True, related_name="reportSubjectId")
    ownerId = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="reportOwnerId")
    creatorId = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="reportCreatorId")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now_add=True)
    media = models.FileField(null=True, blank=True, storage=SupportMediaStorage())

    def __str__(self):
        return self.reportNumber

    class Meta:
        db_table = "Report"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=SupportSubject)
pre_save.connect(slug_save, sender=ReportSubject)
