from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from api.manager import  UserManager
from army_backend.utils import upload_image


class Role:
    STUDENT = 0
    ASSESSOR = 1
    ADMIN = 2

ROLE_CHOICES = [
    (Role.STUDENT, 'Student'),
    (Role.ASSESSOR, 'Assessor'),
    (Role.ADMIN, 'Admin')
]


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    username = models.CharField(max_length=24, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=Role.STUDENT)
    is_staff = models.BooleanField(default=False)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.role == Role.ADMIN

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()


class Category:
    INTERNATIONAL='International'
    NATIONAL='National'
    ECONOMY='Economy'
    DEFENCE='Defence'
    SCIENCE_TECH='Science'


CATEGORY_CHOICES = [
    (Category.INTERNATIONAL, 'INTERNATIONAL'),
    (Category.NATIONAL, 'NATIONAL'),
    (Category.ECONOMY, 'ECONOMY'),
    (Category.DEFENCE, 'DEFENCE'),
    (Category.SCIENCE_TECH, 'SCIENCE_TECH'),
]


class CurrentAffair(models.Model):
    text = models.TextField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default=Category.INTERNATIONAL, max_length=20)

    def __str__(self):
        return str(self.text)


class FreeTest(models.Model):
    email = models.EmailField(verbose_name='Free Test Email', max_length=24)

    def __str__(self):
        return self.email


class HeaderImage(models.Model):
    image = models.ImageField(
        verbose_name='Upload Header Picture', upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.image)
