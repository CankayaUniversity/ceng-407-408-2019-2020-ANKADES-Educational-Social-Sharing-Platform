# Generated by Django 3.0.2 on 2020-04-18 19:25

import ankadescankaya.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='examcategory',
            name='isLecture',
        ),
        migrations.AddField(
            model_name='exam',
            name='media',
            field=models.FileField(blank=True, null=True, storage=ankadescankaya.storage_backends.ExamMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='exam',
            name='lectureCode',
            field=models.CharField(max_length=50),
        ),
    ]
