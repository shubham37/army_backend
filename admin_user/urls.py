from django.contrib import admin
from django.conf.urls import url, include
from admin_user.views import AdminProfile

urlpatterns = [
    url(r'^profile/', AdminProfile.as_view(), name='admin_profle')
]
