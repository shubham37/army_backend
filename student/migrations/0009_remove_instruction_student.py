# Generated by Django 3.1.2 on 2020-11-15 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20201024_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='student',
        ),
    ]
