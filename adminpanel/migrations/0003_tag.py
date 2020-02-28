# Generated by Django 3.0.2 on 2020-02-28 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0002_auto_20200226_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Tag Id')),
                ('title', models.CharField(max_length=254, unique=True, verbose_name='Tag Adı')),
                ('slug', models.SlugField(max_length=254, verbose_name='Slug')),
                ('view', models.PositiveIntegerField(default=0, verbose_name='Tag Görüntülenme')),
                ('isActive', models.BooleanField(default=True, verbose_name='Aktiflik')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulduğu Tarih')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan Kişi')),
            ],
            options={
                'db_table': 'Tag',
                'ordering': ['-createdDate'],
            },
        ),
    ]
