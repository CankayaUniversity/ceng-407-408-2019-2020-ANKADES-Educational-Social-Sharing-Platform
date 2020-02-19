import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models


class MainPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="İzin Id")
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name="İzin Adı")
    name_slug = models.CharField(unique=True, blank=False, null=False, max_length=254, verbose_name="Unique İzin Adı")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.name_slug

    class Meta:
        ordering = ["-created_date"]


class MainGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Main Group Id")
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name="Grup Adı")
    name_slug = models.CharField(unique=True, blank=False, null=False, max_length=254, verbose_name="Unique Grup Adı")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.name_slug

    class Meta:
        ordering = ["-created_date"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = RichTextField(verbose_name="Description", null=True, blank=True)
    image = models.FileField(default='default-user-image.png', null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True, verbose_name="Kullanıcı Admin mi?")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-date_joined"]


class AccountHasPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Hesap İzin Id")
    user_id = models.ForeignKey(Account, verbose_name="Bağlı Olduğu Hesap", on_delete=models.PROTECT)
    permission_id = models.ForeignKey(MainPermission, verbose_name="Bağlı Olduğu İzin", on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")


class AccountGroupPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Account Group Permission Id")
    permission_id = models.ForeignKey(MainPermission, verbose_name="Bağlı Olduğu İzinler", on_delete=models.PROTECT)
    group_id = models.ForeignKey(MainGroup, verbose_name="Bağlı Olduğu Grup", on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Account Group Id")
    user_id = models.ForeignKey(Account, verbose_name="Bağlı Olduğu Hesap", on_delete=models.PROTECT)
    group_id = models.ForeignKey(MainGroup, verbose_name="Bağlı Olduğu Grup", on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")


class AccountSocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sosyal Medya Id")
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Sosyal Medya Adı")
    name_slug = models.CharField(max_length=254, verbose_name="Sosyal Medya Slug")
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.name_slug

    class Meta:
        ordering = ['-created_date']


class SocialMediaUrl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Sosyal Medya Url Id")
    social_media_id = models.ForeignKey(AccountSocialMedia, on_delete=models.CASCADE)
    address = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ['-created_date']


class AccountActivity(models.Model):
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

