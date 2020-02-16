import uuid

from django.db import models


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Course Category Id")
    course_category_title = models.CharField(max_length=254, verbose_name="Course Category Title")
    course_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Course Category Slug")
    course_category_description = models.TextField(verbose_name="Course Category Description", null=True, blank=True)
    course_category_created_date = models.DateTimeField(auto_now_add=True,
                                                         verbose_name="Course Category Created Date")

    def __str__(self):
        return self.course_category_title

    class Meta:
        ordering = ['-course_category_created_date']


class CourseSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Course Sub Category Id")
    course_sub_category_title = models.CharField(max_length=254, verbose_name="Course Sub Category Title")
    course_sub_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Course Sub Category Slug")
    course_sub_category_description = models.TextField(verbose_name="Course Sub Category Description", null=True,
                                                       blank=True)
    course_sub_category_created_date = models.DateTimeField(auto_now_add=True,
                                                            verbose_name="Course Sub Category Created Date")
    course_category_id = models.ForeignKey(CourseCategory, verbose_name="Course Main Category",
                                           on_delete=models.CASCADE)

    def __str__(self):
        return self.course_sub_category_title

    class Meta:
        ordering = ['-course_sub_category_created_date']
