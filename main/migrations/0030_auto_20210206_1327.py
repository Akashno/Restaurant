# Generated by Django 3.1.6 on 2021-02-06 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210206_1318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table',
            old_name='reserverd',
            new_name='reserved',
        ),
    ]