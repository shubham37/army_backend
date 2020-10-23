from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^student_api/', include('student.urls')),
    url(r'^assessor_api/', include('assessor.urls')),
    url(r'^admin_api/', include('admin_user.urls')),
]
