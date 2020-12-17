# Generated by Django 3.1.2 on 2020-12-07 05:33

import army_backend.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_freetest'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=army_backend.utils.upload_image, verbose_name='Upload Header Picture')),
            ],
        ),
    ]
