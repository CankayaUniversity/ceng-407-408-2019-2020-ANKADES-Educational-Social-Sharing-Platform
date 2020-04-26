import uuid

from django.db import models

from account.models import Account
from ankadescankaya.storage_backends import SupportMediaStorage


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    displayMessage = models.CharField(max_length=255, blank=True, null=True)
    supportNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    post = models.CharField(null=False, blank=False, max_length=32, verbose_name="Application Post Number")
    description = models.CharField(max_length=254)
    isActive = models.BooleanField(default=True)
    isRead = models.BooleanField(default=True)
    isSolved = models.BooleanField(default=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="owner")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="creator")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now_add=True)
    media = models.FileField(null=True, blank=True, storage=SupportMediaStorage())

    def __str__(self):
        return self.supportNumber

    class Meta:
        db_table = "Report"
        ordering = ['-createdDate']
