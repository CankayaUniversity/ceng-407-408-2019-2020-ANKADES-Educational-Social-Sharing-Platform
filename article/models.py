import uuid

from ckeditor.fields import RichTextField
from django.db import models

from account.models import Account


class ArticleCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Kategori Id")
    article_category_creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Makale Kategori Başlığı")
    article_category_title = models.CharField(max_length=254, verbose_name="Makale Kategori Başlığı")
    article_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Makale Kategori Slug")
    article_category_description = models.TextField(verbose_name="Makale Kategori Açıklama", null=True, blank=True)
    article_category_created_date = models.DateTimeField(auto_now_add=True,
                                                         verbose_name="Makale Kategori Oluşturulma Tarihi")

    def __str__(self):
        return self.article_category_title

    class Meta:
        ordering = ['-article_category_created_date']


class ArticleSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Makale Alt Kategori Id")
    article_sub_category_creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Makale Yazarı")
    article_sub_category_title = models.CharField(max_length=254, verbose_name="Makale Alt Kategori Başlık")
    article_sub_category_slug = models.SlugField(unique=True, max_length=254, verbose_name="Makale Alt Kategori Slug")
    article_sub_category_description = models.TextField(verbose_name="Makale Alt Kategori Açıklama", null=True,
                                                        blank=True)
    article_sub_category_created_date = models.DateTimeField(auto_now_add=True,
                                                             verbose_name="Makale Oluşturulma Tarihi")
    article_category_id = models.ForeignKey(ArticleCategory, verbose_name="Makale Ana Kategori", on_delete=models.CASCADE)

    def __str__(self):
        return self.article_sub_category_title

    class Meta:
        ordering = ['-article_sub_category_created_date']


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_sub_category_id = models.ManyToManyField(ArticleSubCategory)
    article_title = models.CharField(max_length=254)
    article_slug = models.CharField(max_length=300)
    article_content = RichTextField()


