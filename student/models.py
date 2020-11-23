from django.db import models
from api.models import User
from assessor.models  import Assessor, Department
from army_backend.utils import upload_image


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
    image = models.ImageField(
        verbose_name='Upload Your \nProfile Picture', upload_to=upload_image,
        null=True, blank=True
        # , validators=[image_extension_validator]
    )
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
    image = models.ImageField(
        verbose_name='Upload Question Image', upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.image)


class TestQuestion(models.Model):
    word = models.CharField(max_length=20, blank=True, null=True)
    text = models.CharField(max_length=120, blank=True, null=True)
    images = models.ManyToManyField(TestImages, blank=True)

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


class PIQForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    oir = models.CharField(max_length=56, null=True, blank=True)
    selection_board = models.CharField(max_length=56, null=True, blank=True)
    batch = models.CharField(max_length=56, null=True, blank=True)
    chest = models.CharField(max_length=56, null=True, blank=True)
    roll_no = models.CharField(max_length=56, null=True, blank=True)
    name = models.CharField(max_length=56, null=True, blank=True)
    father = models.CharField(max_length=56, null=True, blank=True)
    maximum_residence = models.CharField(max_length=56, null=True, blank=True)
    present_residence = models.CharField(max_length=56, null=True, blank=True)
    permanent_residence = models.CharField(max_length=56, null=True, blank=True)
    district_hq = models.CharField(max_length=56, null=True, blank=True)
    state_district = models.CharField(max_length=56, null=True, blank=True)
    religion = models.CharField(max_length=56, null=True, blank=True)
    cast = models.CharField(max_length=56, null=True, blank=True)
    mother_tongue = models.CharField(max_length=56, null=True, blank=True)
    dob = models.CharField(max_length=56, null=True, blank=True)
    marital_status = models.CharField(max_length=56, null=True, blank=True)
    parents_alive = models.CharField(max_length=56, null=True, blank=True)
    age_at_time_death = models.CharField(max_length=56, null=True, blank=True)
    father_education = models.CharField(max_length=56, null=True, blank=True)
    father_occupation = models.CharField(max_length=56, null=True, blank=True)
    father_income = models.CharField(max_length=56, null=True, blank=True)
    mother_education = models.CharField(max_length=56, null=True, blank=True)
    mother_occupation = models.CharField(max_length=56, null=True, blank=True)
    mother_income = models.CharField(max_length=56, null=True, blank=True)
    guardian_education = models.CharField(max_length=56, null=True, blank=True)
    guardian_occupation = models.CharField(max_length=56, null=True, blank=True)
    guardian_income = models.CharField(max_length=56, null=True, blank=True)
    sibling1_education = models.CharField(max_length=56, null=True, blank=True)
    sibling1_occupation = models.CharField(max_length=56, null=True, blank=True)
    sibling1_income = models.CharField(max_length=56, null=True, blank=True)
    sibling2_education = models.CharField(max_length=56, null=True, blank=True)
    sibling2_occupation = models.CharField(max_length=56, null=True, blank=True)
    sibling2_income = models.CharField(max_length=56, null=True, blank=True)
    sibling3_education = models.CharField(max_length=56, null=True, blank=True)
    sibling3_occupation = models.CharField(max_length=56, null=True, blank=True)
    sibling3_income = models.CharField(max_length=56, null=True, blank=True)
    institute_matric = models.CharField(max_length=56, null=True, blank=True)
    institute_secondary = models.CharField(max_length=56, null=True, blank=True)
    institute_graduation = models.CharField(max_length=56, null=True, blank=True)
    institute_pg = models.CharField(max_length=56, null=True, blank=True)
    university_matric = models.CharField(max_length=56, null=True, blank=True)
    university_secondary = models.CharField(max_length=56, null=True, blank=True)
    university_graduation = models.CharField(max_length=56, null=True, blank=True)
    university_pg = models.CharField(max_length=56, null=True, blank=True)
    year_matric = models.CharField(max_length=56, null=True, blank=True)
    year_secondary = models.CharField(max_length=56, null=True, blank=True)
    year_graduation = models.CharField(max_length=56, null=True, blank=True)
    year_pg = models.CharField(max_length=56, null=True, blank=True)
    div_matric = models.CharField(max_length=56, null=True, blank=True)
    div_secondary = models.CharField(max_length=56, null=True, blank=True)
    div_graduation = models.CharField(max_length=56, null=True, blank=True)
    div_pg = models.CharField(max_length=56, null=True, blank=True)
    medium_matric = models.CharField(max_length=56, null=True, blank=True)
    medium_secondary = models.CharField(max_length=56, null=True, blank=True)
    medium_graduation = models.CharField(max_length=56, null=True, blank=True)
    medium_pg = models.CharField(max_length=56, null=True, blank=True)
    scholar_matric = models.CharField(max_length=56, null=True, blank=True)
    scholar_secondary = models.CharField(max_length=56, null=True, blank=True)
    scholar_graduation = models.CharField(max_length=56, null=True, blank=True)
    scholar_pg = models.CharField(max_length=56, null=True, blank=True)
    achievement_matric = models.CharField(max_length=56, null=True, blank=True)
    achievement_secondary = models.CharField(max_length=56, null=True, blank=True)
    achievement_graduation = models.CharField(max_length=56, null=True, blank=True)
    achievement_pg = models.CharField(max_length=56, null=True, blank=True)
    age = models.CharField(max_length=56, null=True, blank=True)
    height = models.CharField(max_length=56, null=True, blank=True)
    weight = models.CharField(max_length=56, null=True, blank=True)
    occupation = models.CharField(max_length=56, null=True, blank=True)
    income = models.CharField(max_length=56, null=True, blank=True)
    ncc = models.CharField(max_length=56, null=True, blank=True)
    wing = models.CharField(max_length=56, null=True, blank=True)
    training = models.CharField(max_length=56, null=True, blank=True)
    division = models.CharField(max_length=56, null=True, blank=True)
    certificate = models.CharField(max_length=56, null=True, blank=True)
    game_name = models.CharField(max_length=56, null=True, blank=True)
    game_duration = models.CharField(max_length=56, null=True, blank=True)
    game_place = models.CharField(max_length=56, null=True, blank=True)
    game_achievement = models.CharField(max_length=56, null=True, blank=True)
    hobbies = models.CharField(max_length=56, null=True, blank=True)
    extra_activity_name = models.CharField(max_length=56, null=True, blank=True)
    extra_activity_duration = models.CharField(max_length=56, null=True, blank=True)
    extra_activity_achievement = models.CharField(max_length=56, null=True, blank=True)
    position = models.CharField(max_length=56, null=True, blank=True)
    nature_of_commission = models.CharField(max_length=56, null=True, blank=True)
    services = models.CharField(max_length=56, null=True, blank=True)
    number_chances = models.CharField(max_length=56, null=True, blank=True)
    interview_entry = models.CharField(max_length=56, null=True, blank=True)
    interview_no_place = models.CharField(max_length=56, null=True, blank=True)
    interview_date = models.CharField(max_length=56, null=True, blank=True)
    interview_chest_batch = models.CharField(max_length=56, null=True, blank=True)
