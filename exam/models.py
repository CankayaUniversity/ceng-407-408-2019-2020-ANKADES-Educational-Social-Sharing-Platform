import uuid
from django.db import models
from django.db.models.signals import pre_save

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import ExamMediaStorage, SchoolMediaStorage


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=254, allow_unicode=True, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    media = models.FileField(null=True, blank=True, storage=SchoolMediaStorage())

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "School"


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departmentCode = models.CharField(null=False, blank=False, max_length=50)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    schoolId = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, null=False, blank=False)
    slug = models.SlugField(max_length=254, allow_unicode=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.departmentCode

    def __unicode__(self):
        return self.departmentCode

    class Meta:
        db_table = "Department"


class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lectureCode = models.CharField(null=True, blank=True, max_length=10)
    postNumber = models.CharField(null=True, blank=True, max_length=32, unique=True)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    departmentId = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, null=False, blank=False, verbose_name="Post Title")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.postNumber

    def __unicode__(self):
        return self.postNumber

    class Meta:
        db_table = "Lecture"


class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=254, allow_unicode=True)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return self.slug

    class Meta:
        db_table = "Term"


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examNumber = models.CharField(max_length=32, unique=True)
    lectureId = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True)
    termId = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    owner = models.CharField(null=True, blank=True, max_length=100, verbose_name="Exam Owner Name")
    examDate = models.DateField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    title = models.CharField(max_length=254)
    media = models.FileField(null=True, blank=True, storage=ExamMediaStorage())

    def __str__(self):
        return self.examNumber

    def __unicode__(self):
        return self.examNumber

    class Meta:
        db_table = "Exam"


class LectureExam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examId = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    lectureId = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    termId = models.ForeignKey(Term, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "LectureExam"


pre_save.connect(slug_save, sender=School)
pre_save.connect(slug_save, sender=Department)
pre_save.connect(slug_save, sender=Term)
