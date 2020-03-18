import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from rest_framework.fields import JSONField
from account.models import Account
from ankadescankaya.slug import slug_save


class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    messageNumber = models.PositiveIntegerField(unique=True, auto_created=True, verbose_name="Mesaj Numarası")
    message = JSONField()  # createdDate - isRead - isDeleted - isLiked - message - sender - receiver

    def __str__(self):
        return self.messageNumber

    class Meta:
        db_table = "Messages"
        ordering = ['-messageNumber']


class GroupMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True)
    messageId = models.ForeignKey(Messages, on_delete=models.PROTECT)
    users = models.ManyToManyField(Account, related_name="AccountGroupMessage", db_table="AccountGroupMessage")
    isBlocked = models.BooleanField(null=True, blank=True, default=False)
    isDeleted = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("group_message_detail", kwargs={"slug": self.slug})

    # def get_like_url(self):
    #     return reverse("like-toggle", kwargs={"slug": self.slug})
    #
    # def get_api_like_url(self):
    #     return reverse("like-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        db_table = "GroupMessages"
        ordering = ['-createdDate']


class DirectMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    isBlocked = models.BooleanField(null=True, blank=True, default=False)
    isDeleted = models.BooleanField(default=False)
    users = models.ManyToManyField(Account, related_name="AccountDirectMessage", db_table="AccountDirectMessage")
    messageId = models.ForeignKey(Messages, on_delete=models.PROTECT)

    class Meta:
        db_table = "DirectMessages"
        ordering = ['-createdDate']

    # def get_absolute_url(self):
    #     return reverse("direct_message_detail", kwargs={"messageNumber": self.messageNumber})
    #
    # def get_api_url(self):
    #     return reverse("direct-message-api-detail", kwargs={"messageNumber": self.messageNumber})


pre_save.connect(slug_save, sender=GroupMessages)
