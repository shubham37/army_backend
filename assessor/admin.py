# accounts.admin.py

from django.contrib import admin
from assessor.models import Assessor, Availability, Briefcase


admin.site.register(Availability)
admin.site.register(Assessor)
admin.site.register(Briefcase)
