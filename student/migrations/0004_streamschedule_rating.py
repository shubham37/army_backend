# Generated by Django 3.1.2 on 2020-10-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_streamschedule_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamschedule',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
