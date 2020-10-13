from rest_framework import  serializers
from student.models import State, City, Pincode, PostOffice, Address, TestSchedule, Test


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id','state_name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields ='__all__'
        depth = 1


class PincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields ='__all__'
        depth = 2


class PostofficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields ='__all__'
        depth = 3


class TestScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSchedule
        fields ='__all__'
        depth = 1



