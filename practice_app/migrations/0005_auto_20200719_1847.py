# Generated by Django 3.0.3 on 2020-07-19 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0004_auto_20200719_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='DOB',
            new_name='Dob',
        ),
    ]
