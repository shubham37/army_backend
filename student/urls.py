from django.contrib import admin
from django.conf.urls import url, include
from api.views import Signup, Login,  ForgotPassword, ResetPassword
from rest_framework.routers import DefaultRouter
from student.views import StateViewSet, CityViewSet,  PincodeViewSet,  PostofficeViewSet,TestScheduleViewSet

router = DefaultRouter()

urlpatterns = []


router.register(r'state', StateViewSet)
router.register(r'city', CityViewSet)
router.register(r'pincode', PincodeViewSet)
router.register(r'postoffice', PostofficeViewSet)
router.register(r'testschedule', TestScheduleViewSet)

urlpatterns += router.urls