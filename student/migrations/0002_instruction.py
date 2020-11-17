# Generated by Django 3.1.2 on 2020-10-23 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessor', '0002_auto_20201023_0723'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.TextField(blank=True, null=True, verbose_name='Instruction By Assessor')),
                ('assessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessor.assessor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]