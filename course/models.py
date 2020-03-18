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
        return self.title

    class Meta:
        db_table = "CourseCategory"
        ordering = ['-createdDate']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT)
    categoryId = models.ForeignKey(CourseCategory, on_delete=models.PROTECT)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField()
    media = models.FileField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isPrivate = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Course"
        ordering = ['-createdDate']


class CourseSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    description = RichTextField()
    updatedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    isActive = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseSection"


class CourseLecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=254)
    description = RichTextField()
    sectionId = models.ForeignKey(CourseSection, on_delete=models.PROTECT)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    isActive = models.BooleanField(default=True)
    media = models.FileField()
    isQuiz = models.BooleanField(default=False)
    question = RichTextField()
    answer = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CourseLecture"


class CourseComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseId = models.ForeignKey(Course, on_delete=models.PROTECT)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.PROTECT)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.PROTECT)
    isRoot = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "CourseComment"
        ordering = ['-createdDate']


class CourseTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tagId = models.ForeignKey(Tag, on_delete=models.PROTECT)
    courseId = models.ForeignKey(Course, on_delete=models.PROTECT)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.tagId

    class Meta:
        db_table = "CourseTag"


pre_save.connect(slug_save, sender=CourseCategory)
pre_save.connect(slug_save, sender=Course)
pre_save.connect(slug_save, sender=CourseSection)
pre_save.connect(slug_save, sender=CourseLecture)