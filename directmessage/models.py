import uuid

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.urls import reverse
from rest_framework.fields import JSONField

from account.models import Account


class DirectMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kişi", related_name="user")
    message = RichTextField()
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme")
    messageNumber = models.PositiveIntegerField(unique=True, auto_created=True, verbose_name="Mesaj Numarası")
    isBlocked = models.BooleanField(null=True, blank=True, default=False, verbose_name="Engelli")
    isRoot = models.BooleanField(null=True, blank=True, default=False)
    isRead = models.BooleanField(blank=True, null=True, verbose_name="Okunma", default=False)
    isReply = models.BooleanField(default=False, verbose_name="Yanıt mı?")
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ebevynlik")
    isDeleted = models.BooleanField(default=False, verbose_name="Silinen")
    likes = models.ManyToManyField(Account, related_name="LikedMessages", default=0, blank=True)

    def __str__(self):
        return self.messageNumber

    class Meta:
        db_table = "DirectMessage"
        ordering = ['-createdDate']

    def __unicode__(self):
        return self.messageNumber

    def get_absolute_url(self):
        return reverse("direct_message_detail", kwargs={"messageNumber": self.messageNumber})

    def get_api_url(self):
        return reverse("direct-message-api-detail", kwargs={"messageNumber": self.messageNumber})