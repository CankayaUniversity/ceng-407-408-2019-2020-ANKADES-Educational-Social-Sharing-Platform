# Generated by Django 3.0.2 on 2020-02-26 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminactivity',
            name='activityCreator',
            field=models.CharField(max_length=254, verbose_name='Oluşturan Kişi'),
        ),
    ]
