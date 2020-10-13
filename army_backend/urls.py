from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^student/', include('student.urls')),
    url(r'assessor/', include('assessor.urls')),
]
