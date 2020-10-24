from rest_framework import  serializers
from student.models import Student, State, City, Pincode, PostOffice, \
    Address, SecurityQuestion, Occupation, StreamSchedule, TestImages, \
        TestQuestion, Test, TestSubmission, ProgressReport, Instruction
        


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields ='__all__'
        depth = 1


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields ='__all__'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields ='__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = ['first_name','middle_name','last_name']


class StreamScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamSchedule
        fields ='__all__'
        depth = 1


class TestImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImages
        fields ='__all__'


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields ='__all__'
        depth = 1


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        depth = 1


class TestSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSubmission
        fields = '__all__'
        depth = 1


class TestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSubmission
        fields = '__all__'
        depth = 1


class ProgressReportSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProgressReport
        fields = '__all__'


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = '__all__'
        depth = 1