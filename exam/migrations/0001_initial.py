# Generated by Django 3.0.2 on 2020-02-28 19:52

import ckeditor.fields
from django.conf import settings
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
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Bölüm Id')),
                ('title', models.CharField(max_length=254, verbose_name='Bölüm Adı')),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Bölüm Adı Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Bölüm Açıklama ')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Bölüm Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Bölüm Güncellendiği Tarih')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('media', models.FileField(default='default-user-image.png', upload_to='', verbose_name='Dosya')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Bölüm Oluşturan Kişi')),
            ],
            options={
                'db_table': 'Department',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Sınav Sorusu Id')),
                ('title', models.CharField(max_length=254, verbose_name='Sınav Sorusu Başlık')),
                ('description', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Sınav Sorusu Slug')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Sınav Sorusu Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Sınav Sorusu Güncellendiği Tarih')),
                ('media', models.FileField(default='default-user-image.png', upload_to='', verbose_name='Dosya')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Görüntülenme Sayısı')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Sınav Sorusu Oluşturan')),
                ('departmentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Department', verbose_name='Bölüm Adı')),
            ],
            options={
                'db_table': 'Exam',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Dönem Id')),
                ('term', models.CharField(max_length=254, verbose_name='Dönem (Bahar-Kış)')),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Dönem Slug')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Dönem Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Dönem Güncellendiği Tarih')),
                ('departmentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Department', verbose_name='Bölüm')),
            ],
            options={
                'db_table': 'Term',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Sınav Soruları Id')),
                ('title', models.CharField(max_length=254, verbose_name='Okul Adı')),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Okul Adı Slug')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Okul Açıklama')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Okul Oluşturulma Tarihi')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Güncellendiği Tarih')),
                ('since', models.DateTimeField(verbose_name='Okul Kurulduğu Tarih')),
                ('media', models.FileField(default='default-user-image.png', upload_to='')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Okul Oluşturan Kişi')),
            ],
            options={
                'db_table': 'School',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Sınav Sorusu Id')),
                ('title', models.CharField(max_length=254, verbose_name='Sınav Sorusu Başlık')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=254, unique=True, verbose_name='Sınav Sorusu Slug')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Sınav Sorusu Oluşturulduğu Tarih')),
                ('updatedDate', models.DateTimeField(blank=True, null=True, verbose_name='Sınav Sorusu Güncellendiği Tarih')),
                ('media', models.FileField(default='default-user-image.png', upload_to='', verbose_name='Dosya')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Görüntülenme Sayısı')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Sınav Sorusu Oluşturan')),
                ('departmentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Department', verbose_name='Bölüm Adı')),
                ('termId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Term', verbose_name='Dönem')),
            ],
            options={
                'db_table': 'Lecture',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='ExamTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Makale Tag Id')),
                ('examId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Exam', verbose_name='Makale')),
                ('tagId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminpanel.Tag')),
            ],
            options={
                'db_table': 'ExamTag',
            },
        ),
        migrations.CreateModel(
            name='ExamComment',
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
                ('media', models.FileField(default='default-user-image.png', upload_to='', verbose_name='Dosya')),
                ('examId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.Exam', verbose_name='Makale Yorumcusu')),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cevap', to='exam.ExamComment')),
            ],
            options={
                'db_table': 'ExamComment',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.AddField(
            model_name='department',
            name='schoolId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.School', verbose_name='Okul Adı'),
        ),
    ]
