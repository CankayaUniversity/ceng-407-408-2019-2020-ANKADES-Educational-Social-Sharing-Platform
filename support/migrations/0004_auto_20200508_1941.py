# Generated by Django 3.0.2 on 2020-05-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_auto_20200508_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportsubject',
            name='title',
            field=models.CharField(max_length=254),
        ),
    ]
