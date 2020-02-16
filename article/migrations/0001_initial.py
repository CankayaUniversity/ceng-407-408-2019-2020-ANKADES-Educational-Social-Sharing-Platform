# Generated by Django 3.0.2 on 2020-02-15 20:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Article Category Id')),
                ('article_category_title', models.CharField(max_length=254, verbose_name='Article Category Title')),
                ('article_category_slug', models.SlugField(max_length=254, unique=True, verbose_name='Article Category Slug')),
                ('article_category_description', models.TextField(blank=True, null=True, verbose_name='Article Category Description')),
                ('article_category_created_date', models.DateTimeField(auto_now_add=True, verbose_name='Article Category Created Date')),
            ],
            options={
                'ordering': ['-article_category_created_date'],
            },
        ),
        migrations.CreateModel(
            name='ArticleSubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Article Sub Category Id')),
                ('article_sub_category_title', models.CharField(max_length=254, verbose_name='Article Sub Category Title')),
                ('article_sub_category_slug', models.SlugField(max_length=254, unique=True, verbose_name='Article Sub Category Slug')),
                ('article_sub_category_description', models.TextField(blank=True, null=True, verbose_name='Article Sub Category Description')),
                ('article_sub_category_created_date', models.DateTimeField(auto_now_add=True, verbose_name='Article Sub Category Created Date')),
                ('article_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleCategory', verbose_name='Course Main Category')),
            ],
            options={
                'ordering': ['-article_sub_category_created_date'],
            },
        ),
    ]
