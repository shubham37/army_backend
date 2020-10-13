from rest_framework.routers import DefaultRouter
from assessor.views import AvailabilityViewSet, BriefcaseViewSet

router = DefaultRouter()

urlpatterns = []


router.register(r'availablity', AvailabilityViewSet)
router.register(r'breifcase', BriefcaseViewSet)

urlpatterns += router.urls