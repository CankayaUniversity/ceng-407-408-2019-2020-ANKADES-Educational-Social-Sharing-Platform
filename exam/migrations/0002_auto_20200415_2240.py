# Generated by Django 3.0.2 on 2020-04-15 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountschool',
            name='schoolId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.School'),
        ),
        migrations.AlterField(
            model_name='accountschool',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exam',
            name='lectureId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.School', verbose_name='Dersi'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='examcomment',
            name='examId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.Exam'),
        ),
        migrations.AlterField(
            model_name='examcomment',
            name='parentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.ExamComment'),
        ),
        migrations.AlterField(
            model_name='school',
            name='parentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.School'),
        ),
    ]
