# Generated by Django 3.0.2 on 2020-04-10 11:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminActivity',
            new_name='AdminLogs',
        ),
        migrations.AlterModelTable(
            name='adminlogs',
            table='AdminLogs',
        ),
    ]
