from django.contrib import admin
from api.models import User, CurrentAffair, HeaderImage, \
    RollOfHonor, CustomerQuery, VideoContent, Notification


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','date_joined', 'role')
    list_filter = ('role',)
    ordering =('-date_joined',)


admin.site.register(User, UserAdmin)
admin.site.register(CurrentAffair)
admin.site.register(HeaderImage)
admin.site.register(RollOfHonor)
admin.site.register(CustomerQuery)
admin.site.register(VideoContent)
admin.site.register(Notification)
