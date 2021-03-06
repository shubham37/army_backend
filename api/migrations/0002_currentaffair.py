# Generated by Django 3.1.2 on 2020-11-20 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentAffair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('category', models.IntegerField(choices=[(1, 'INTERNATIONAL'), (2, 'NATIONAL'), (3, 'ECONOMY'), (4, 'DEFENCE'), (5, 'SCIENCE_TECH')], default=1)),
            ],
        ),
    ]
