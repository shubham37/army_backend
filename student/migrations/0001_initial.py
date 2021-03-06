# Generated by Django 3.1.2 on 2020-10-22 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_block', models.CharField(max_length=24)),
                ('street', models.CharField(blank=True, max_length=24, null=True)),
                ('area', models.CharField(blank=True, max_length=48, null=True)),
                ('phone', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(max_length=20, verbose_name='Occupation')),
            ],
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.CharField(max_length=6)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.city')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Security Question')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('middle_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, max_length=64, null=True)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1)),
                ('dob', models.DateField(verbose_name='DOB')),
                ('marital_status', models.IntegerField(choices=[(1, 'Single'), (2, 'Married')], default=1)),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile Number')),
                ('security_answer', models.CharField(max_length=48)),
                ('plan', models.IntegerField(choices=[(0, 'None'), (1, 'DIAMOND'), (2, 'GOLD'), (3, 'SILVER'), (4, 'INSTITUTIONAL')], default=0)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.address')),
                ('occupation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.occupation')),
                ('security_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.securityquestion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Test')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessor.department')),
            ],
        ),
        migrations.CreateModel(
            name='TestImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='question image')),
            ],
        ),
        migrations.CreateModel(
            name='TestSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Test Answer')),
                ('submission_status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Done')], default=1)),
                ('remark', models.CharField(blank=True, max_length=96, null=True, verbose_name='Remarks')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('checking_status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Done')], default=1)),
                ('submission_date', models.DateField(auto_now_add=True, verbose_name='date joined')),
                ('assessor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessor.assessor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, max_length=20, null=True)),
                ('text', models.CharField(blank=True, max_length=120, null=True)),
                ('images', models.ManyToManyField(blank=True, null=True, to='student.TestImages')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.testquestion'),
        ),
        migrations.CreateModel(
            name='StreamSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('subject', models.CharField(max_length=128)),
                ('video_url', models.TextField(blank=True, null=True, verbose_name='video room url')),
                ('assessor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.related.ForeignKey, to='assessor.assessor')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.related.ForeignKey, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.TextField(verbose_name='report')),
                ('reporting_date', models.DateField(auto_now_add=True, verbose_name='date joined')),
                ('assessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessor.assessor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='PostOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_name', models.CharField(max_length=64)),
                ('pincode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.pincode')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.state'),
        ),
        migrations.AddField(
            model_name='address',
            name='post_office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.postoffice'),
        ),
    ]
