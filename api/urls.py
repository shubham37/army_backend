from django.contrib import admin
from django.conf.urls import url, include
from api.views import Signup, Login,  ForgotPassword, ResetPassword

urlpatterns = [
    url(r'^signup/', Signup.as_view(), name='signup_student'),
    url(r'^login/', Login.as_view(), name='login_student'),
    url(r'^forgot_password/', ForgotPassword.as_view(), name='forgot_password_link'),
    url(r'^reset_password/', ResetPassword.as_view(), name='reset_password'),
]
