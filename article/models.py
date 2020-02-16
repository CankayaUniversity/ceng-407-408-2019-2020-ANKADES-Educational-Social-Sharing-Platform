import uuid

from django.db import models


class ArticleCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Article Category Id")
    article_category_title = models.CharField(max_length=254, verbose_name="Article Category Title")
    article_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Article Category Slug")
    article_category_description = models.TextField(verbose_name="Article Category Description", null=True, blank=True)
    article_category_created_date = models.DateTimeField(auto_now_add=True,
                                                         verbose_name="Article Category Created Date")

    def __str__(self):
        return self.article_category_title

    class Meta:
        ordering = ['-article_category_created_date']


class ArticleSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Article Sub Category Id")
    article_sub_category_title = models.CharField(max_length=254, verbose_name="Article Sub Category Title")
    article_sub_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Article Sub Category Slug")
    article_sub_category_description = models.TextField(verbose_name="Article Sub Category Description", null=True,
                                                        blank=True)
    article_sub_category_created_date = models.DateTimeField(auto_now_add=True,
                                                             verbose_name="Article Sub Category Created Date")
    article_category_id = models.ForeignKey(ArticleCategory, verbose_name="Course Main Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.article_sub_category_title

    class Meta:
        ordering = ['-article_sub_category_created_date']
