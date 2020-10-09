from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.manager import  UserManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True,)
    username = models.CharField(max_length=24, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()


class Gender:
    MALE=1
    FEMALE=2
    OTHER=3


class MaritalStatus:
    SINGLE=1
    MARRIED=2


class Department:
    PP=1
    IO=2
    PSYCH=3


DEPARTMENT_CHOICES = [
    (Department.PP, 'PP'),
    (Department.IO, 'IO')
]

MARITAL_STATUS_CHOICES = [
    (MaritalStatus.SINGLE, 'Single'),
    (MaritalStatus.MARRIED, 'Married')
]

GENDER_CHOICES = [
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female'),
    (Gender.OTHER, 'Other')
]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Gender.MALE)
    dob = models.DateField(verbose_name='DOB')
    occupation = models.CharField(max_length=128)
    marital_status = models.IntegerField(choices=MARITAL_STATUS_CHOICES, default=MaritalStatus.SINGLE)
    mobile = models.IntegerField(verbose_name='Mobile Number')
    address = models.TextField(verbose_name='address')
    post_office = models.CharField(max_length=128)
    phone = models.IntegerField(verbose_name='Phone')

    def get_full_name(self):
        return str(self.first_name+self.middle_name+self.last_name)

    def __str__(self):
        return str(self.first_name)


class Assessor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Gender.MALE)
    department = models.IntegerField(choices=DEPARTMENT_CHOICES, default=Department.PP)

    def get_full_name(self):
        return str(self.first_name+self.middle_name+self.last_name)

    def __str__(self):
        return str(self.first_name)


class TestSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.ForeignKey, null=True, blank=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')


class Test(models.Model):
    identifier = models.CharField(verbose_name='Test', max_length=10)
    student = models.ForeignKey(Student, on_delete=models.ForeignKey, null=True, blank=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    remark = models.CharField(verbose_name='Remarks', max_length=96)
    comment = models.CharField(verbose_name='Comment', max_length=96)

    def __str__(self):
        return str(self.identifier)

