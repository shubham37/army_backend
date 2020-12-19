# Generated by Django 3.1.2 on 2020-12-19 08:03

import army_backend.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customerquery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VideoContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to=army_backend.utils.upload_file, verbose_name='Upload Your File')),
                ('tag', models.CharField(choices=[('Training', 'Training'), ('Practice', 'Practice')], default='Training', max_length=10)),
                ('category', models.CharField(choices=[('OIR', 'OIR'), ('PP', 'PP'), ('GD', 'GD'), ('PSYCH', 'PSYCH'), ('GTO', 'GTO'), ('IO', 'IO'), ('PD', 'PD'), ('SE', 'SE'), ('DFS1S2', 'DFS1S2'), ('DAD', 'DAD')], default='OIR', max_length=10)),
            ],
        ),
    ]
