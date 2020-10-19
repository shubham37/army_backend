from rest_framework import  serializers
from student.models import Student, State, City, Pincode, PostOffice, \
    Address, StreamSchedule, Test, PsychTestQuestion


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


class StreamScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamSchedule
        fields ='__all__'
        depth = 1


class TestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = ['first_name','middle_name','last_name']


class PsychTestQustionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PsychTestQuestion
        fields = '__all__'
