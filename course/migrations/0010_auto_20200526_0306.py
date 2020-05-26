# Generated by Django 3.0.2 on 2020-05-26 00:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0009_auto_20200526_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursevideo',
            name='likes',
            field=models.ManyToManyField(blank=True, db_table='AccountLikedCourseVideo', default=0, related_name='courseVideoLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
