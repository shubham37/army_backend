import uuid
import datetime
from django.db import models
from api.models  import User, Role
from army_backend.utils import upload_image, upload_file

class Gender:
    MALE=1
    FEMALE=2
    OTHER=3

GENDER_CHOICES = [
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female'),
    (Gender.OTHER, 'Other')
]


class Department(models.Model):
    name = models.CharField(verbose_name='Department Name', max_length=64)
    code = models.CharField(verbose_name='Department Code', max_length=10)

    def save(self, *args, **kwargs):
        if len(self.code.split(' '))<=1:
            super().save(*args,**kwargs)
        else:
            raise  ValueError("Code Not allowed spaces.")

    def __str__(self):
        return str(self.name)


class Position(models.Model):
    designation = models.CharField(verbose_name='Designation', max_length=64)

    def __str__(self):
        return str(self.designation)


class Assessor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(
        verbose_name='Upload Your \nProfile Picture', upload_to=upload_image,
        null=True, blank=True
        # , validators=[image_extension_validator]
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Gender.MALE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.user and (self.user.role == Role.ASSESSOR):
            super().save(*args,**kwargs)
        else:
            raise  ValueError("User has not permission to become Assessor.")

    def get_full_name(self):
        return str(self.first_name+self.middle_name+self.last_name)

    def __str__(self):
        return str(self.first_name)
    
class Status:
    AVAILABLE=1
    NOT_AVAILABLE=2

STATUS_CHOICES = [
    (Status.AVAILABLE, 'Available'),
    (Status.NOT_AVAILABLE, 'Not Available')
]

class Availability(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')
    status = models.IntegerField(choices=STATUS_CHOICES, default=Status.AVAILABLE)

    def str(self):
        return str(self.assessor)


class Briefcase(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    file = models.FileField(
        verbose_name='Upload Your File', upload_to=upload_file,
        null=True, blank=True
    )
    title = models.CharField(max_length=50, default='Unknown', null=True, blank=True)
    extention = models.CharField(max_length=10, default='mp4', null=True, blank=True)
    size = models.IntegerField(verbose_name='Size in KB', default=0)


    def str(self):
        return str(self.file)
