from django.contrib import admin
from django.conf.urls import url, include
from api.views import Signup, Login,  ForgotPassword, ResetPassword
from rest_framework.routers import DefaultRouter
from student.views import StateViewSet, CityViewSet,  PincodeViewSet,  \
    PostofficeViewSet, StreamScheduleViewSet, StudentProfile, PsychTest, \
        PsychQuestion, Test

router = DefaultRouter()

urlpatterns = [
    url(r'^profile/', StudentProfile.as_view(), name='student_profle'),
    url(r'^tests/', PsychTest.as_view(), name='psych_tests'),
    url(r'^test_question/(?P<code>\D+)/', PsychQuestion.as_view(), name='test_question')
]

router.register(r'dept_test', Test)
router.register(r'state', StateViewSet)
router.register(r'city', CityViewSet)
router.register(r'pincode', PincodeViewSet)
router.register(r'postoffice', PostofficeViewSet)
router.register(r'assessor_stream_schedule', StreamScheduleViewSet)

urlpatterns += router.urls