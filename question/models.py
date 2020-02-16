import uuid

from django.db import models


class QuestionCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Question Category Id")
    question_category_title = models.CharField(max_length=254, verbose_name="Question Category Title")
    question_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Question Category Slug")
    question_category_description = models.TextField(verbose_name="Question Category Description", null=True,
                                                     blank=True)
    question_category_created_date = models.DateTimeField(auto_now_add=True,
                                                          verbose_name="Question Category Created Date")

    def __str__(self):
        return self.question_category_title

    class Meta:
        ordering = ['-question_category_created_date']


class QuestionSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Question Sub Category Id")
    question_sub_category_title = models.CharField(max_length=254, verbose_name="Question Sub Category Title")
    question_sub_category_slug = models.SlugField(unique=True, max_length=254,
                                                  verbose_name="Question Sub Category Slug")
    question_sub_category_description = models.TextField(verbose_name="Question Sub Category Description", null=True,
                                                         blank=True)
    question_sub_category_created_date = models.DateTimeField(auto_now_add=True,
                                                              verbose_name="Question Sub Category Created Date")
    question_category_id = models.ForeignKey(QuestionCategory, verbose_name="Question Main Category",
                                             on_delete=models.CASCADE)

    def __str__(self):
        return self.question_sub_category_title

    class Meta:
        ordering = ['-question_sub_category_created_date']
