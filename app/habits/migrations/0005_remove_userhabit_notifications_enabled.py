# Generated by Django 5.1.1 on 2024-10-26 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_difficulty_level_alter_userhabit_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userhabit',
            name='notifications_enabled',
        ),
    ]
