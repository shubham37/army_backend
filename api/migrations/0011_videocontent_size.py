# Generated by Django 3.1.2 on 2020-12-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_videocontent_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocontent',
            name='size',
            field=models.IntegerField(default=0, verbose_name='Size in KB'),
        ),
    ]