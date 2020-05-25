# Generated by Django 3.0.2 on 2020-05-25 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0005_auto_20200526_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courselecture',
            name='media',
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.CharField(blank=True, max_length=100, null=True)),
                ('videoNumber', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('view', models.PositiveIntegerField(default=0)),
                ('isPrivate', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('lectureId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.CourseLecture')),
                ('likes', models.ManyToManyField(blank=True, db_table='AccountLikedCourse', default=0, related_name='courseLikes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CourseVideo',
            },
        ),
    ]
