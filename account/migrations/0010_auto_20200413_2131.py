# Generated by Django 3.0.2 on 2020-04-13 18:31

import ankadescankaya.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.FileField(default='default-user-image.png', storage=ankadescankaya.storage_backends.UserMediaStorage(), upload_to=''),
        ),
    ]
