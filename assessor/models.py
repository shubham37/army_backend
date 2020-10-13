from django.db import models
from api.models  import User


class Department:
    GTO='GTO'
    IO='IO'
    PSYCH='PSYCH'
    PD='PD'
    IT='IT'


class Gender:
    MALE=1
    FEMALE=2
    OTHER=3

class Position:
    HOD=1
    COLONEL=2
    BRIG=3


POSITION_CHOICES = [
    (Position.HOD, 'HOD'),
    (Position.COLONEL, 'COLONEL'),
    (Position.BRIG, 'BRIG')
]

GENDER_CHOICES = [
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female'),
    (Gender.OTHER, 'Other')
]

DEPARTMENT_CHOICES = [
    (Department.GTO, 'GTO Department'),
    (Department.IO, 'IO Department'),
    (Department.PSYCH, 'PSYCH Department'),
    (Department.PD, 'PD Department'),
    (Department.IT, 'Intt Test Department')
]


class Assessor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Gender.MALE)
    department = models.CharField(max_length=5, choices=DEPARTMENT_CHOICES, default=Department.PSYCH)
    position = models.IntegerField(choices=POSITION_CHOICES, default=Position.HOD)

    def save(self, *args, **kwargs):
        if self.user and self.user.is_staff:
            super().save(*args,**kwargs)
        else:
            raise  ValueError("User has not permission to become Assessor.")

    def get_full_name(self):
        return str(self.first_name+self.middle_name+self.last_name)

    def __str__(self):
        return str(self.first_name)

    
class Availability(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')

    def str(self):
        return str(self.assessor)


class Briefcase(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    document_url = models.URLField(verbose_name='document')
    document_name = models.CharField(max_length=48)

    def str(self):
        return str(self.assessor)
