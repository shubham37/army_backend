from django.contrib import admin
from api.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','date_joined', 'role')
    list_filter = ('role',)
    ordering =('-date_joined',)


admin.site.register(User, UserAdmin)
