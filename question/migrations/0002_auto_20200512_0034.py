# Generated by Django 3.0.2 on 2020-05-11 21:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncategory',
            name='title',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='questioncategory',
            name='updatedDate',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
