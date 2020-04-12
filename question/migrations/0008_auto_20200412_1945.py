# Generated by Django 3.0.2 on 2020-04-12 16:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0007_question_introduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(blank=True, db_table='AccountLikedQuestion', default=0, related_name='questionLikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='likes',
            field=models.ManyToManyField(blank=True, db_table='AccountLikedQuestionComment', default=0, related_name='questionCommentLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
