# accounts.admin.py

from django.contrib import admin
from assessor.models import Department, Position, Assessor, \
    Availability, Briefcase


admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Assessor)
admin.site.register(Availability)
admin.site.register(Briefcase)
