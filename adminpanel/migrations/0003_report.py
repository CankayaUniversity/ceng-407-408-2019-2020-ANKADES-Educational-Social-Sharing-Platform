# Generated by Django 3.0.2 on 2020-04-14 00:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_auto_20200410_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=254, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=254)),
                ('description', models.CharField(max_length=254)),
                ('isActive', models.BooleanField(default=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Report',
                'ordering': ['-createdDate'],
            },
        ),
    ]
