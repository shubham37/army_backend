from rest_framework import  serializers
from assessor.models import Availability, Briefcase

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields ='__all__'
        depth = 1


class BriefcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Briefcase
        fields ='__all__'
        depth = 1
