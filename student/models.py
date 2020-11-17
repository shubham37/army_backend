from django.db import models
from api.models import User
from assessor.models  import Assessor, Department


class State(models.Model):
    state_name = models.CharField(max_length=48)

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=48)

    def __str__(self):
        return self.city_name


class Pincode(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.pincode


class PostOffice(models.Model):
    pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE)
    po_name = models.CharField(max_length=64)

    def __str__(self):
        return self.po_name


class Address(models.Model):
    flat_block = models.CharField(max_length=24)
    street = models.CharField(max_length=24, null=True, blank=True)
    area = models.CharField(max_length=48, null=True, blank=True)
    phone = models.CharField(max_length=6)
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.area) + " " + str(self.phone)


class Gender:
    MALE=1
    FEMALE=2
    OTHER=3


class MaritalStatus:
    SINGLE=1
    MARRIED=2


class MembershipPlan:
    NO=0
    DIAMOND=1
    GOLD=2
    SILVER=3
    INSTITUTIONAL=4


MEMBERSHIP_PLAN_CHOICES = [
    (MembershipPlan.NO, 'None'),
    (MembershipPlan.DIAMOND, 'DIAMOND'),
    (MembershipPlan.GOLD, 'GOLD'),
    (MembershipPlan.SILVER, 'SILVER'),
    (MembershipPlan.INSTITUTIONAL, 'INSTITUTIONAL'),
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

class SecurityQuestion(models.Model):
    question = models.TextField(verbose_name='Security Question')

    def __str__(self):
        return self.question

class Occupation(models.Model):
    occupation = models.CharField(verbose_name='Occupation', max_length=20)

    def __str__(self):
        return self.occupation


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Gender.MALE)
    dob = models.DateField(verbose_name='DOB')
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    marital_status = models.IntegerField(choices=MARITAL_STATUS_CHOICES, default=MaritalStatus.SINGLE)
    mobile = models.CharField(max_length=10, verbose_name='Mobile Number')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    security_question = models.ForeignKey(SecurityQuestion, on_delete=models.CASCADE)
    security_answer = models.CharField(max_length=48)
    plan = models.IntegerField(choices=MEMBERSHIP_PLAN_CHOICES, default=MembershipPlan.NO)

    def get_full_name(self):
        return str(self.first_name+self.middle_name+self.last_name)

    def __str__(self):
        return str(self.first_name) + str(self.middle_name) + str(self.last_name)


class StreamStatus:
    PENDING = 1
    COMPLETED = 2
    EXPIRED = 3

STREAMSTATUS_CHOICES = [
    (StreamStatus.PENDING, 'Pending'),
    (StreamStatus.COMPLETED, 'Complete'),
    (StreamStatus.EXPIRED, 'Expired')
]

class StreamSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.ForeignKey, null=True, blank=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.ForeignKey, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')
    subject = models.CharField(max_length=128)
    video_url = models.TextField(verbose_name='video room url', null=True, blank=True)
    status = models.IntegerField(choices=STREAMSTATUS_CHOICES, default=StreamStatus.PENDING)
    rating = models.IntegerField(default=0)
    remark = models.CharField(verbose_name='Remarks', max_length=96, null=True, blank=True)
    comment = models.TextField(verbose_name='Comment',null=True, blank=True)

    def __str__(self):
        return str(self.subject) + '--' + str(self.assessor.department)

class Status:
    PENDING=1
    DONE=2


STATUS_CHOICES = [
    (Status.PENDING, 'Pending'),
    (Status.DONE, 'Done'),
]

class TestImages(models.Model):
    image = models.URLField(verbose_name='question image')

    def __str__(self):
        return str(self.image)


class TestQuestion(models.Model):
    word = models.CharField(max_length=20, blank=True, null=True)
    text = models.CharField(max_length=120, blank=True, null=True)
    images = models.ManyToManyField(TestImages, blank=True)

    # def save(self, *args, **kwargs):
    #     if (self.word and self.text) or (self.images and self.text) or (self.word and self.images):
    #         raise  ValueError("Set Only One Thing For Test Question")
    #     else:
    #         super().save(*args,**kwargs)

    def __str__(self):
        if self.word:
            return str(self.word)
        if self.text:
            return str(self.text)
        if self.images:
            return str('images')


class Test(models.Model):
    code = models.CharField(verbose_name='Test', max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    question_display_time = models.IntegerField(default=0)
    answer_display_time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.code)


class TestSubmission(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.TextField(verbose_name='Test Answer', null=True, blank=True)
    submission_status = models.IntegerField(choices=STATUS_CHOICES, default=Status.PENDING)
    remark = models.CharField(verbose_name='Remarks', max_length=96, null=True, blank=True)
    comment = models.TextField(verbose_name='Comment',null=True, blank=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE, null=True, blank=True)
    checking_status = models.IntegerField(choices=STATUS_CHOICES, default=Status.PENDING)
    submission_date = models.DateField(verbose_name='date joined', auto_now_add=True)

    def __str__(self):
        return str(self.test) + "--" + str(self.student)


class ProgressReport(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student,  on_delete=models.CASCADE)
    report = models.TextField(verbose_name='report')
    reporting_date = models.DateField(verbose_name='date joined', auto_now_add=True)

    def  __str__(self):
        return self.assessor + " -- " + self.student

class Instruction(models.Model):
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE)
    # student = models.ForeignKey(Student,  on_delete=models.CASCADE)
    instruction = models.TextField(verbose_name='Instruction By Assessor', null=True, blank=True)

    # def  __str__(self):
    #     return self.assessor
