# Generated by Django 3.1.2 on 2020-12-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessor', '0005_auto_20201123_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='briefcase',
            name='extention',
            field=models.CharField(blank=True, default='mp4', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='briefcase',
            name='title',
            field=models.CharField(blank=True, default='Unknown', max_length=50, null=True),
        ),
    ]
