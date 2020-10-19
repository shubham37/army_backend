from django.contrib import admin
from student.models import Student, StreamSchedule, Test,\
    State, City, Pincode, PostOffice, Address, \
        PsychTestQuestion, PsychTestSubmission, ProgressReport


admin.site.register(State)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(PostOffice)
admin.site.register(Address)
admin.site.register(Student)
admin.site.register(StreamSchedule)
admin.site.register(Test)
admin.site.register(PsychTestQuestion)
admin.site.register(PsychTestSubmission)
admin.site.register(ProgressReport)
