from rest_framework import  serializers
from assessor.models import Availability, Briefcase, Assessor, \
    Department, Position


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class AssessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessor
        fields ='__all__'
        depth = 1


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields ='__all__'


class BriefcaseSerializer(serializers.ModelSerializer):
    def validate(self, attr):
        import ipdb; ipdb.set_trace()
    class Meta:
        model = Briefcase
        fields ='__all__'
