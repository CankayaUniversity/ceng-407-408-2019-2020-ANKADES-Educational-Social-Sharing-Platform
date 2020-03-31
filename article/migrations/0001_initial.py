# Generated by Django 3.0.2 on 2020-03-18 17:32

import ckeditor.fields
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=254)),
                ('slug', models.SlugField(allow_unicode=True, max_length=254, unique=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('media', models.FileField(blank=True, null=True, upload_to='')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('view', models.PositiveIntegerField(default=0)),
                ('isActive', models.BooleanField(default=True)),
                ('isPrivate', models.BooleanField(blank=True, default=False, null=True)),
                ('readTime', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Article',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('view', models.PositiveIntegerField(default=0)),
                ('like', models.PositiveIntegerField(default=0)),
                ('isActive', models.BooleanField(default=True)),
                ('articleId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.Article')),
                ('tagId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adminpanel.Tag')),
            ],
            options={
                'db_table': 'ArticleTag',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', ckeditor.fields.RichTextField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('isRoot', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('view', models.PositiveIntegerField(default=0)),
                ('like', models.PositiveIntegerField(default=0)),
                ('articleId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.Article')),
                ('creator', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='articleCommentId', to='article.ArticleComment')),
            ],
            options={
                'db_table': 'ArticleComment',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=254)),
                ('slug', models.SlugField(allow_unicode=True, max_length=254, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('isRoot', models.BooleanField(default=False)),
                ('tree', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(default=dict), blank=True, default=list, max_length=200, size=None)),
                ('view', models.PositiveIntegerField(default=0)),
                ('isActive', models.BooleanField(default=True)),
                ('isCategory', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.ArticleCategory')),
            ],
            options={
                'db_table': 'ArticleCategory',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleCategory'),
        ),
        migrations.AddField(
            model_name='article',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, db_table='AccountLikedArticle', default=0, related_name='articleLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
