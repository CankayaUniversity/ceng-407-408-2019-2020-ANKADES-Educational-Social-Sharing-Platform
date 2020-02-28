import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="İzin Id")
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name="İzin Adı")
    slug = models.CharField(unique=True, blank=False, null=False, max_length=254, verbose_name="Unique İzin Adı")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="İzin Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="İzin Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Permission"
        ordering = ["-createdDate"]


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Grup Id")
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name="Grup Adı")
    slug = models.CharField(unique=True, blank=False, null=False, max_length=254, verbose_name="Unique Grup Adı")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Grup Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Grup Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Group"
        ordering = ["-createdDate"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = RichTextField(verbose_name="Biyografi", null=True, blank=True)
    image = models.FileField(default='default-user-image.png', verbose_name="Profil Resmi")
    view = models.PositiveIntegerField(default=0, verbose_name="Makale Görüntülenme Tarihi", null=True, blank=True)
    updatedDate = models.DateTimeField(verbose_name="Hesap Güncellendiği Tarih", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Account"
        ordering = ["-date_joined"]


class AccountPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Hesap İzin Id")
    userId = models.ForeignKey(Account, verbose_name="Bağlı Olduğu Hesap", on_delete=models.SET_NULL, null=True)
    permissionId = models.ForeignKey(Permission, verbose_name="Bağlı Olduğu İzin", on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Hesap İzni Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Hesap İzni Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "AccountPermission"
        ordering = ["-createdDate"]


class GroupPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Account Group Permission Id")
    permissionId = models.ForeignKey(Permission, verbose_name="İzin Adı", on_delete=models.SET_NULL, null=True)
    groupId = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Grup Adı")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Grup İzni Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Grup İzni Güncellendiği Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.permissionId

    class Meta:
        db_table = "GroupPermission"
        ordering = ["-createdDate"]


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Account Group Id")
    userId = models.ForeignKey(Account, verbose_name="Kullanıcı Adı", on_delete=models.SET_NULL, null=True)
    groupId = models.ForeignKey(Group, verbose_name="Grup Adı", on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Hesap Grup Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Hesap Grup Oluşturulduğu Tarih", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "AccountGroup"
        ordering = ["-createdDate"]


class AccountActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Aktivite Id")
    activityCreator = models.CharField(max_length=254, verbose_name="Oluşturan Kişi")
    activityTitle = models.CharField(max_length=254, verbose_name="Başlık")
    activityApplication = models.CharField(max_length=254, verbose_name="Uygulama")
    activityDescription = models.CharField(max_length=254, verbose_name="Açıklama")
    activityMethod = models.CharField(max_length=254, verbose_name="Method Türü")
    activityCreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    activityUpdatedDate = models.DateTimeField(verbose_name="Güncellendiği Tarih", null=True, blank=True)

    def __str__(self):
        return self.activityCreator

    class Meta:
        db_table = "AccountActivity"
        ordering = ['-activityCreatedDate']

