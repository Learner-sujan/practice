# Generated by Django 3.0.3 on 2020-07-17 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='Birthday',
            field=models.CharField(max_length=50),
        ),
    ]
