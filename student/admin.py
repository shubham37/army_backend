from django.contrib import admin
from student.models import Student, State, City, Pincode, PostOffice, \
    Address, SecurityQuestion, Occupation, StreamSchedule, TestImages, \
        TestQuestion, Test, TestSubmission, ProgressReport, Instruction, PIQForm


admin.site.register(Student)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(PostOffice)
admin.site.register(Address)
admin.site.register(SecurityQuestion)
admin.site.register(Occupation)
admin.site.register(StreamSchedule)
admin.site.register(TestImages)
admin.site.register(TestQuestion)
admin.site.register(Test)
admin.site.register(TestSubmission)
admin.site.register(ProgressReport)
admin.site.register(Instruction)
admin.site.register(PIQForm)
