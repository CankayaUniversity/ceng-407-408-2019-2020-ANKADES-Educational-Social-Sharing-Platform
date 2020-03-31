import uuid

from django.db import models
from django.urls import reverse
from rest_framework.fields import JSONField

from account.models import Account


class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Subject")
    messageNumber = models.CharField(unique=True, max_length=32)
    isInbox = models.BooleanField(null=True, blank=True, default=False)
    isSent = models.BooleanField(null=True, blank=True, default=False)
    isDraft = models.BooleanField(null=True, blank=True, default=False)
    isTrash = models.BooleanField(null=True, blank=True, default=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    message = JSONField()  # createdDate - isRead - isDeleted - isLiked - message - sender - receiver

    def __str__(self):
        return self.messageNumber

    def __unicode__(self):
        return self.messageNumber

    # def get_absolute_url(self):
    #     return reverse("account_detail", kwargs={"messageNumber": self.messageNumber})
    #
    # def get_like_url(self):
    #     return reverse("follower-toggle", kwargs={"messageNumber": self.messageNumber})
    #
    # def get_api_like_url(self):
    #     return reverse("follower-api-toggle", kwargs={"messageNumber": self.messageNumber})

    class Meta:
        db_table = "Mail"
        ordering = ["-date_joined"]


class AccountMail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    receiver = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="receiver")
    sender = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="sender")
    mailId = models.ForeignKey(Mail)

    class Meta:
        db_table = "AccountMail"
        ordering = ["-date_joined"]
