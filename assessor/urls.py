from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from assessor.views import AvailabilityViewSet, BriefcaseViewSet, \
    AssessorDept, AssessorProfile

router = DefaultRouter()

urlpatterns = [
    url(r'^dept/(?P<dep>\D+)/', AssessorDept.as_view(), name='dept_assessor_list'),
    url(r'^profile/', AssessorProfile, name='assessor_profile')
]


router.register(r'availablity', AvailabilityViewSet)
router.register(r'breifcase', BriefcaseViewSet)

urlpatterns += router.urls