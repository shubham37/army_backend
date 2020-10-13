# accounts.admin.py

from django.contrib import admin
from api.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','is_active','date_joined')
    list_filter = ('is_student','is_staff','is_superuser')
    ordering =('-date_joined',)



admin.site.register(User, UserAdmin)
