# Generated by Django 3.0.2 on 2020-04-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_articlecomment_isreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='postNumber',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]
