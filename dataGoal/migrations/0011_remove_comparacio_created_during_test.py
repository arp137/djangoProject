# Generated by Django 5.0.2 on 2024-05-13 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataGoal', '0010_comparacio_created_during_test_alter_comparacio_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparacio',
            name='created_during_test',
        ),
    ]