import uuid

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.PROTECT)
    isRoot = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "CourseCategory"
        ordering = ['-createdDate']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseNumber = models.CharField(unique=True, null=True, blank=True, max_length=32)
    categoryId = models.ForeignKey(CourseCategory, on_delete=models.PROTECT)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField()
    introduction = models.CharField(max_length=254, null=True, blank=True)
    coursePicture = models.FileField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isPrivate = models.BooleanField(default=False)
    enrolledAccount = models.ManyToManyField(Account, related_name="enrolledAccount", default=0, blank=True,
                                             db_table="AccountCourse")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Course"
        ordering = ['-createdDate']


class CourseLecture(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    courseId = models.ForeignKey(Course, on_delete=models.PROTECT)
    sectionTitle = models.CharField(max_length=100, null=True, blank=True)
    sectionSlug = models.SlugField(unique=True, allow_unicode=True)
    sectionDescription = RichTextField()
    sectionCreatedDate = models.DateTimeField(auto_now_add=True)
    sectionUpdatedDate = models.DateTimeField(null=True, blank=True)
    #
    lectureParent = models.ForeignKey('self', on_delete=models.PROTECT)
    lectureNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    lectureTitle = models.CharField(null=True, blank=True, max_length=100)
    lectureDescription = RichTextField()
    lectureCreatedDate = models.DateTimeField(auto_now_add=True)
    lectureUpdatedDate = models.DateTimeField(null=True, blank=True)
    lectureView = models.PositiveIntegerField(default=0, null=True, blank=True)
    lectureMedia = models.FileField(null=True, blank=True)
    isLecturePrivate = models.BooleanField(default=True)

    def __str__(self):
        return self.lectureNumber

    class Meta:
        db_table = "CourseLecture"


class CourseComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseId = models.ForeignKey(Course, on_delete=models.PROTECT)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.PROTECT)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, related_name="articleCommentId", on_delete=models.PROTECT)
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
pre_save.connect(slug_save, sender=CourseLecture)
