# Generated by Django 3.0.2 on 2020-05-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200523_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='introduction',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
