import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group, Permission
from django.db import models

from account.models import Account


class AdminActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Kurs Id")
    act_creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Oluşturan Kişi")
    act_title = models.CharField(max_length=254, verbose_name="Başlık")
    act_app = models.CharField(max_length=254, verbose_name="Uygulama")
    act_desc = models.CharField(max_length=254, verbose_name="Açıklama")
    act_method = models.CharField(max_length=254, verbose_name="Method Türü")
    act_created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")

    def __str__(self):
        return self.act_creator

    class Meta:
        ordering = ['-act_created_date']

# class Teacher(Group):
#
# class Student(Group):
