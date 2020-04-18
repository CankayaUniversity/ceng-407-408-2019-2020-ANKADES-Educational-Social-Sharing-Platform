# Generated by Django 3.0.2 on 2020-04-18 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20200418_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=254)),
                ('slug', models.SlugField(allow_unicode=True, max_length=254, unique=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Skill',
                'ordering': ['-createdDate'],
            },
        ),
        migrations.CreateModel(
            name='AccountSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('skillId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Skill')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'AccountSkill',
            },
        ),
    ]
