import uuid

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import CourseMediaStorage


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    isRoot = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseCategory"
        ordering = ['-createdDate']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseNumber = models.CharField(unique=True, null=True, blank=True, max_length=32)
    categoryId = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField()
    introduction = models.CharField(max_length=254, null=True, blank=True)
    coursePicture = models.FileField(null=True, blank=True, storage=CourseMediaStorage(), default="no-image-available.png")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isPrivate = models.BooleanField(default=False)
    enrolledAccount = models.ManyToManyField(Account, related_name="enrolledAccount", default=0, blank=True,
                                             db_table="AccountEnrolledCourse")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Course"
        ordering = ['-createdDate']


class CourseSection(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(allow_unicode=True)
    description = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isPrivate = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "CourseSection"
        ordering = ['-createdDate']


class CourseLecture(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sectionId = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    lectureNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    slug = models.SlugField(allow_unicode=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    description = RichTextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0, null=True, blank=True)
    media = models.FileField(null=True, blank=True)
    isPrivate = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "CourseLecture"


class CourseComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseId = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    isRoot = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "CourseComment"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=CourseCategory)
pre_save.connect(slug_save, sender=Course)
pre_save.connect(slug_save, sender=CourseSection)
pre_save.connect(slug_save, sender=CourseLecture)
