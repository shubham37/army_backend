# Generated by Django 3.1.2 on 2020-11-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201120_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentaffair',
            name='category',
            field=models.CharField(choices=[('International', 'INTERNATIONAL'), ('National', 'NATIONAL'), ('Economy', 'ECONOMY'), ('Defence', 'DEFENCE'), ('Science', 'SCIENCE_TECH')], default='International', max_length=20),
        ),
    ]
