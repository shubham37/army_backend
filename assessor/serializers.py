from rest_framework import  serializers
from assessor.models import Availability, Briefcase, Assessor


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields ='__all__'


class BriefcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Briefcase
        fields ='__all__'


class AssessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessor
        fields ='__all__'
