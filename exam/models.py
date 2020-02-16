import uuid

from django.db import models

from account.models import Account


class ExamSchool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Exam Category Id")
    exam_school_title = models.CharField(max_length=254, verbose_name="Exam Category Title")
    exam_school_slug = models.SlugField(unique=True, max_length=254, verbose_name="Exam Category Slug")
    exam_school_description = models.TextField(verbose_name="Exam Category Description", null=True,
                                               blank=True)
    exam_school_created_date = models.DateTimeField(auto_now_add=True,
                                                    verbose_name="Exam Category Created Date")

    def __str__(self):
        return self.exam_school_title

    class Meta:
        ordering = ['-exam_school_created_date']


class ExamDepartment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Exam Sub Category Id")
    exam_department_title = models.CharField(max_length=254, verbose_name="Exam Sub Category Title")
    exam_department_slug = models.SlugField(unique=True, max_length=254,
                                            verbose_name="Exam Sub Category Slug")
    exam_department_description = models.TextField(verbose_name="Exam Sub Category Description", null=True,
                                                   blank=True)
    exam_department_created_date = models.DateTimeField(auto_now_add=True,
                                                        verbose_name="Exam Sub Category Created Date")
    exam_school_id = models.ForeignKey(ExamSchool, verbose_name="Exam Main Category",
                                       on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_department_title

    class Meta:
        ordering = ['-exam_department_created_date']


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Exam Id")
    exam_author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Exam Author")
    exam_title = models.CharField(max_length=254, verbose_name="Exam Title")
    exam_slug = models.SlugField(unique=True, max_length=254, verbose_name="Exam Title Slug")
    exam_created_date = models.DateTimeField(auto_now_add=True,
                                             verbose_name="Exam Created Date")
    exam_school_id = models.ForeignKey(ExamDepartment, verbose_name="Exam Department",
                                       on_delete=models.CASCADE)
    exam_media = models.FileField(null=True, blank=True, verbose_name="Exam File")
    exam_view = models.PositiveIntegerField(default=0, verbose_name="Exam View Count")

    def __str__(self):
        return self.exam_title

    class Meta:
        ordering = ['-exam_created_date']
