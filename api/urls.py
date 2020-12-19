from django.conf.urls import url, include
from api.views import Signup, Login, ForgotPassword, \
    ResetPassword, LogOut, Plan, SendOTP, CurrentAffairView, \
        AssessorStar, HeaderImagesView, ContactView, VideoView


urlpatterns = [
    url(r'^signup/', Signup.as_view(), name='signup_student'),
    url(r'^select_plan/', Plan.as_view(), name='select_plan'),
    url(r'^login/', Login.as_view(), name='login_student'),
    url(r'^forgot_password/', ForgotPassword.as_view(), name='forgot_password_link'),
    url(r'^reset_password/', ResetPassword.as_view(), name='reset_password'),
    url(r'^logout/', LogOut.as_view(), name='logout'),
    url(r'^send_otp/', SendOTP.as_view(), name='send_otp'),
    url(r'^current_affair/(?P<cat>\D+)/', CurrentAffairView.as_view(), name='current_affair'),
    url(r'^stars/', AssessorStar.as_view(), name='star_of_the_day'),
    url(r'^contact/', ContactView.as_view(), name='contact_form'),
    url(r'^images/', HeaderImagesView.as_view(), name='header_images'),
    url(r'^videos/(?P<cat>\D+)/', VideoView.as_view(), name='videos'),
]
