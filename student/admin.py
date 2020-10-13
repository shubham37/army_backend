# accounts.admin.py

from django.contrib import admin
from student.models import Student, TestSchedule, Test, State, City, Pincode, PostOffice, Address


admin.site.register(State)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(PostOffice)
admin.site.register(Address)
admin.site.register(Student)
admin.site.register(TestSchedule)
admin.site.register(Test)
