# Generated by Django 5.1.1 on 2024-10-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='milestones',
            field=models.IntegerField(default=0),
        ),
    ]