import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import UserMediaStorage


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(null=False, blank=False, max_length=100)
    slug = models.CharField(unique=True, blank=False, null=False, max_length=254)
    description = models.CharField(max_length=254, null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("admin_edit_permission", kwargs={"slug": self.slug})

    def get_active_url(self):
        return reverse("permission-active-toggle", kwargs={"slug": self.slug})

    def get_active_api_url(self):
        return reverse("permission-active-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        db_table = "Permission"
        ordering = ["-createdDate"]


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(null=False, blank=False, max_length=100)
    slug = models.CharField(unique=True, blank=False, null=False, max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("admin_edit_group", kwargs={"slug": self.slug})

    def get_active_url(self):
        return reverse("group-active-toggle", kwargs={"slug": self.slug})

    def get_active_api_url(self):
        return reverse("group-active-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        db_table = "Group"
        ordering = ["-createdDate"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cv = RichTextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=254)
    graduate = models.TextField(null=True, blank=True, max_length=254)
    image = models.FileField(default='default-user-image.png', storage=UserMediaStorage())
    backgroundImage = models.FileField(default='photo1.png')
    view = models.PositiveIntegerField(default=0, null=True, blank=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=True)
    is_admin = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"username": self.username})

    class Meta:
        db_table = "Account"
        ordering = ["-date_joined"]


class AccountFollower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    followerId = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="followerId")
    followingId = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="followingId")

    class Meta:
        db_table = "AccountFollow"


class AccountPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permissionId = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "AccountPermission"


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "AccountGroup"


class SocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "SocialMedia"
        ordering = ["slug"]


class AccountSocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)
    socialMediaId = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    socialMediaUsername = models.CharField(null=True, blank=True, max_length=32)

    class Meta:
        db_table = "AccountSocialMedia"


class Zones(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE)
    isCountry = models.BooleanField(default=False)
    isCity = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Zones"
        ordering = ['-createdDate']


class AccountZones(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)
    zoneId = models.ForeignKey(Zones, on_delete=models.CASCADE)

    class Meta:
        db_table = "AccountZones"


class AccountLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    application = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    method = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "AccountLogs"
        ordering = ['-createdDate']


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    application = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    method = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "Notification"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=SocialMedia)
pre_save.connect(slug_save, sender=Group)
pre_save.connect(slug_save, sender=Permission)
