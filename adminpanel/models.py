import uuid

from django.db import models

from account.models import Account


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Id")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    activity = models.CharField(max_length=254, verbose_name="Başlık")
    activity_application = models.CharField(max_length=254, verbose_name="Uygulama")
    activity_description = models.CharField(max_length=254, verbose_name="Açıklama")
    activity_action = models.CharField(max_length=254, verbose_name="Method Türü")
    activity_created_date = models.DateTimeField(auto_now_add=True, verbose_name="Kurs Oluşturulduğu Tarih")

    def __str__(self):
        return self.creator

    class Meta:
        ordering = ['-activity_created_date']