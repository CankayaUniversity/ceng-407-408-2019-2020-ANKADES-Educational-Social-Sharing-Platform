# Generated by Django 3.0.2 on 2020-03-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_auto_20200307_2333'),
        ('exam', '0004_auto_20200308_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examtag',
            name='tagId',
            field=models.ManyToManyField(to='adminpanel.Tag', verbose_name='Etiket'),
        ),
    ]
