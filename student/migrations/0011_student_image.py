# Generated by Django 3.1.2 on 2020-11-22 05:58

import army_backend.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_piqform'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=army_backend.utils.upload_image, verbose_name='Upload Your \nProfile Picture'),
        ),
    ]
