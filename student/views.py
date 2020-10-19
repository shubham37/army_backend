from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from assessor.models import Assessor
from student.models import State, City, Pincode, PostOffice, StreamSchedule, \
    Test, Student, PsychTestSubmission,PsychTestQuestion
from student.serializers import  StateSerializer, CitySerializer, \
    PincodeSerializer, PostofficeSerializer, StreamScheduleSerializer, \
        TestStatusSerializer, StudentSerializer, PsychTestQustionSerializer
from api.permissions import  IsStudentAuthenticated


class StateViewSet(ViewSet):
    queryset = State.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StateSerializer

    def get_object(self, request, id):
        cities = City.objects.filter(state_id=id)
        return cities

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            states = serialize.data
            is_success = True
        else:
            states = None
            is_success = False

        context = {
            "is_success": is_success,
            "states": states
        }
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cities = self.get_object(request, pk)
        if cities.exists():
            serialized = CitySerializer(cities, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("State Has No City", status=status.HTTP_404_NOT_FOUND)


class CityViewSet(ViewSet):
    queryset = City.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    def get_object(self, request, id):
        pincodes = Pincode.objects.filter(city_id=id)
        return pincodes

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            cities = serialize.data
            is_success = True
        else:
            cities = None
            is_success = False

        context = {
            "is_success": is_success,
            "cities": cities
        }
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        pincodes = self.get_object(request, pk)
        if pincodes.exists():
            serialized = PincodeSerializer(pincodes, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("City has No Pincode.", status=status.HTTP_404_NOT_FOUND)


class PincodeViewSet(ViewSet):
    queryset = Pincode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PincodeSerializer

    def get_object(self, request, id):
        postoffices = PostOffice.objects.filter(pincode_id=id)
        return postoffices

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            pin_codes = serialize.data
            is_success = True
        else:
            pin_codes = None
            is_success = False

        context = {
            "is_success": is_success,
            "pin_codes": pin_codes
        }
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        postoffices = self.get_object(request, pk)
        if postoffices.exists():
            serialized = PostofficeSerializer(postoffices, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Pincode has No Post Office.", status=status.HTTP_404_NOT_FOUND)


class PostofficeViewSet(ViewSet):
    queryset = PostOffice.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostofficeSerializer

    def get_object(self, request, id):
        postoffice = self.queryset.filter(id=id)
        return postoffice

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            post_offices = serialize.data
            is_success = True
        else:
            post_offices = None
            is_success = False

        context = {
            "is_success": is_success,
            "post_offices": post_offices
        }
        return Response(context, status=status.HTTP_200_OK)


class StreamScheduleViewSet(ViewSet):
    queryset = StreamSchedule.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = StreamScheduleSerializer

    def get_object(self, request, id):
        StreamSchedule = self.queryset.filter(id=id)
        return StreamSchedule

    # list of collection related to user
    @action(detail=True,methods=['GET'])
    def student_list(self, request, pk=None):
        query_set = self.queryset.filter(student_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            StreamSchedules = serialize.data
            is_success = True
        else:
            StreamSchedules = None
            is_success = False

        context = {
            "is_success": is_success,
            "StreamSchedules": StreamSchedules
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(detail=True,methods=['GET'])
    def assessor_list(self, request, pk=None):
        query_set = self.queryset.filter(assessor_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            StreamSchedules = serialize.data
            is_success = True
        else:
            StreamSchedules = None
            is_success = False

        context = {
            "is_success": is_success,
            "StreamSchedules": StreamSchedules
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsStudentAuthenticated,])
    def add_test_schedule(self, request):
        schedules = request.data.get('schedules')
        assessor = request.data.get('assessor')
        user = request.user
        try:
            assessor = Assessor.objects.get(id = assessor)
            student = Student.objects.get(user=user)

            StreamSchedule.objects.filter(assessor=assessor, student=student).delete()
            for schedule in schedules:
                schedule['student'] = student
                schedule['assessor'] = assessor
                serialize = self.serializer_class(schedule)
                try:
                    if serialize.is_valid():
                        serialize.save()
                except Exception as e:
                    print(e)
            return Response(data={"detail":"Data Update Successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(data={"error":e}, status=status.HTTP_304_NOT_MODIFIED)

    @action(detail=False, methods=['GET'], permission_classes=[IsStudentAuthenticated, ])
    def student_schedule(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Exception as e:
            return Response(data={"detail":e}, status=status.HTTP_401_UNAUTHORIZED)

        schedules = self.queryset.filter(student=student)
        serialized_schedule = self.serializer_class(schedules, manny=True)

        return Response(data=serialized_schedule.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        StreamSchedule = self.get_object(request, pk)
        if StreamSchedule.exists():
            serialized = StreamScheduleSerializer(StreamSchedule, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("No Data.", status=status.HTTP_404_NOT_FOUND)


class Test(ViewSet):
    queryset = Test.objects.all()
    permission_classes = (IsStudentAuthenticated,)
    serializer_class = TestStatusSerializer

    @action(detail=False, methods=['POST'])
    def test_status(self, request):
        serialize = self.serializer_class(self.queryset, many=True)
        return Response(data={'status':serialize.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def test_reports(self, request):
        serialize = self.serializer_class(self.queryset, many=True)
        return Response(data={'reports':serialize.data}, status=status.HTTP_200_OK)


class StudentProfile(APIView):
    permission_classes = [IsStudentAuthenticated, ]
    serializer_class = StudentSerializer

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Exception as e:
            return Response(data={'detail':e},status=status.HTTP_401_UNAUTHORIZED)

        serialize = self.serializer_class(student)
        return Response(data=serialize.data,status=status.HTTP_200_OK)


class PsychTest(APIView):
    permission_classes = [IsStudentAuthenticated, ]

    def post(self, request, code):
        test_ans = request.data
        test_code = code

        try:
            student = Student.objects.get(user=request.user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            test_submission = PsychTestSubmission.objects.create(
                code=test_code, student=student, answer=test_ans
            )
            return Response(data={'detail':"Test Submitted Successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PsychQuestion(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PsychTestQustionSerializer

    def get(self, request, code):
        try:
            test_question = PsychTestQuestion.objects.filter(
                code=test_code
            )
            serialize = self.serializer_class(test_question)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
