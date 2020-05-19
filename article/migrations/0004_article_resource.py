# Generated by Django 3.0.2 on 2020-05-19 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='resource',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
