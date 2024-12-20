# Generated by Django 5.1.1 on 2024-11-06 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0006_remove_habit_skills_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userhabit',
            name='next_milestone',
        ),
        migrations.AlterField(
            model_name='habitlog',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userhabit',
            name='status',
            field=models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('ABANDONED', 'Abandoned')], default='IN_PROGRESS', max_length=50),
        ),
    ]
