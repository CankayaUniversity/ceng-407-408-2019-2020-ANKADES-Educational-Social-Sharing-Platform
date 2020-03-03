# Generated by Django 3.0.2 on 2020-03-03 13:02

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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Makale Id')),
                ('title', models.CharField(max_length=254, verbose_name='Makale Başlığı')),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Makale Slug')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Makale Açıklaması')),
                ('media', models.FileField(blank=True, null=True, upload_to='', verbose_name='Makale Dosya Yükleme')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Makale Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Makale Güncellendiği Tarih')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Makale Görüntülenme Tarihi')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('isPrivate', models.BooleanField(default=False, verbose_name='Özellik')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='Makale Beğeni Sayısı')),
            ],
            options={
                'db_table': 'Article',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Makale Tag Id')),
                ('articleId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.Article', verbose_name='Makale')),
                ('tagId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminpanel.Tag')),
            ],
            options={
                'db_table': 'ArticleTag',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Yorum Id')),
                ('creator', models.CharField(max_length=50, verbose_name='Kullanıcı Adı')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Yorum')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('isRoot', models.BooleanField(default=False, verbose_name='Root Durumu')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Yorum Görüntülenme Tarihi')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='Yorum Beğeni Sayısı')),
                ('articleId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.Article', verbose_name='Makale Yorumcusu')),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cevap', to='article.ArticleComment')),
            ],
            options={
                'db_table': 'ArticleComment',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Makale Kategori Id')),
                ('title', models.CharField(max_length=254, verbose_name='Makale Kategori Başlığı')),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Makale Kategori Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Makale Kategori Açıklama')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Makale Kategori Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Makale Kategori Güncellendiği Tarih')),
                ('isRoot', models.BooleanField(default=False, verbose_name='Root Durumu')),
                ('tree', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(default=dict), blank=True, default=list, max_length=200, size=None)),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Makale Görüntülenme Tarihi')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan Kişi')),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.ArticleCategory', verbose_name='Üst Kategorisi')),
            ],
            options={
                'db_table': 'ArticleCategory',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categoryId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.ArticleCategory', verbose_name='Makale Kategori'),
        ),
        migrations.AddField(
            model_name='article',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Makale Öğretmeni'),
        ),
    ]
