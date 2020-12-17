from django.contrib import admin
from api.models import User, CurrentAffair, HeaderImage


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','date_joined', 'role')
    list_filter = ('role',)
    ordering =('-date_joined',)


admin.site.register(User, UserAdmin)
admin.site.register(CurrentAffair)
admin.site.register(HeaderImage)
