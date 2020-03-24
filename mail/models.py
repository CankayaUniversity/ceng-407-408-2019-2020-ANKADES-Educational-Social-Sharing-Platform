import uuid

from django.db import models


class MailMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")


class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Subject")
    slug = models.SlugField(allow_unicode=True)
    isInbox = models.BooleanField(null=True, blank=True, default=False)
    isSent = models.BooleanField(null=True, blank=True, default=False)
    isDraft = models.BooleanField(null=True, blank=True, default=False)
    isTrash = models.BooleanField(null=True, blank=True, default=False)
