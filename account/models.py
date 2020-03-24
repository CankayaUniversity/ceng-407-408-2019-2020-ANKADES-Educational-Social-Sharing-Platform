import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from ankadescankaya.slug import slug_save


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(null=False, blank=False, max_length=100)
    slug = models.CharField(unique=True, blank=False, null=False, max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

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
        return reverse("active-toggle", kwargs={"slug": self.slug})

    def get_active_api_url(self):
        return reverse("active-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        db_table = "Group"
        ordering = ["-createdDate"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = RichTextField(null=True, blank=True)
    image = models.FileField(default='default-user-image.png')
    backgroundImage = models.FileField(default='photo1.png')
    view = models.PositiveIntegerField(default=0, null=True, blank=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    follower = models.ManyToManyField('self', related_name="follower", default=0, db_table="AccountFollower")
    email = models.EmailField(unique=True, null=False, blank=True)
    is_admin = models.BooleanField(null=True, blank=True, default=False, verbose_name="Is Admin?")

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"username": self.username})

    def get_like_url(self):
        return reverse("follower-toggle", kwargs={"username": self.username})

    def get_api_like_url(self):
        return reverse("follower-api-toggle", kwargs={"username": self.username})

    class Meta:
        db_table = "Account"
        ordering = ["-date_joined"]


class GroupPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groupId = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)
    permissionId = models.ForeignKey(Permission, on_delete=models.PROTECT)

    class Meta:
        db_table = "GroupPermission"


class AccountPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groupId = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)
    userId = models.ForeignKey(Account, on_delete=models.PROTECT)

    class Meta:
        db_table = "AccountPermission"


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    groupId = models.ForeignKey(Group, on_delete=models.PROTECT)
    userId = models.ForeignKey(Account, on_delete=models.PROTECT)

    class Meta:
        db_table = "AccountGroup"


class SocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    media = models.FileField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "SocialMedia"
        ordering = ["-createdDate"]


class AccountSocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(Account, on_delete=models.PROTECT)
    socialMediaId = models.ForeignKey(SocialMedia, on_delete=models.PROTECT)

    class Meta:
        db_table = "AccountSocialMedia"


class Zones(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.PROTECT)
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
    userId = models.ForeignKey(Account, on_delete=models.PROTECT)
    zoneId = models.ForeignKey(Zones, on_delete=models.PROTECT)

    class Meta:
        db_table = "AccountZones"


class AccountActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT)
    title = models.CharField(max_length=254)
    slug = models.SlugField()
    application = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    method = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "AccountActivity"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=SocialMedia)
pre_save.connect(slug_save, sender=Group)
pre_save.connect(slug_save, sender=Permission)
