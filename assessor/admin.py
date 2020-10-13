# accounts.admin.py

from django.contrib import admin
from assessor.models import Assessor, Availability


admin.site.register(Availability)
admin.site.register(Assessor)
