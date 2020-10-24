from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from assessor.views import AvailabilityViewSet, BriefcaseViewSet, \
    AssessorDept, AssessorProfile, DepartmentViewSet, PositionViewSet, \
        AssessorInstruction, TestChecking, Rating

router = DefaultRouter()

urlpatterns = [
    url(r'^dept/(?P<dep>\D+)/', AssessorDept.as_view(), name='dept_assessor_list'),
    url(r'^profile/', AssessorProfile.as_view(), name='assessor_profile')
]


router.register(r'availablity', AvailabilityViewSet)
router.register(r'breifcase', BriefcaseViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'position', PositionViewSet)
router.register(r'instructions', AssessorInstruction)
router.register(r'tests_check', TestChecking)
router.register(r'ratings', Rating)

urlpatterns += router.urls
