import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from assessor.models import Assessor, Availability
from student.models import State, City, Pincode, PostOffice, StreamSchedule, \
    Test, Student, PsychTestSubmission,PsychTestQuestion
from student.serializers import  StateSerializer, CitySerializer, \
    PincodeSerializer, PostofficeSerializer, StreamScheduleSerializer, \
        TestStatusSerializer, TestReportSerializer, StudentSerializer, \
            PsychTestQustionSerializer
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

    # Call from Student on Training Schedule Tab to list of streamSchedules
    def list(self, request):
        query_set = self.queryset.filter(student__user=request.user)
        StreamSchedules = []
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            StreamSchedules = serialize.data
        context = {
            "StreamSchedules": StreamSchedules
        }
        return Response(data=context, status=status.HTTP_200_OK)

    # Call from Student on Schedule for Today Tab to list of today streamSchedules
    @action(detail=False, methods=['GET'], permission_classes=[IsStudentAuthenticated,])
    def today(self, request):
        today = datetime.datetime.today()
        query_set = self.queryset.filter(student__user=request.user, start_time__date=today)
        StreamSchedules = []
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            StreamSchedules = serialize.data
        context = {
            "StreamSchedules": StreamSchedules
        }
        return Response(data=context, status=status.HTTP_200_OK)

    # Call from Student on Dept wise Assessor Tab to add list of streamSchedules
    @action(detail=False, methods=['POST'], permission_classes=[IsStudentAuthenticated,])
    def add_test_schedule(self, request):
        # import ipdb; ipdb.set_trace()
        schedules = request.data.get('schedules')
        assessor = request.data.get('assessor')
        user = request.user
        try:
            assessor = Assessor.objects.get(id = assessor)
            student = Student.objects.get(user=user)
            ss_for_create = []
            for schedule in schedules:
                av = Availability.objects.filter(id= schedule.get('Id'), status=1)
                if av.exists():
                    ss = StreamSchedule(
                        student = student,
                        assessor = assessor,
                        start_time = av.last().start_time,
                        end_time = av.last().end_time,
                        subject= schedule.get('Subject')
                    )
                    av.delete()
                    ss_for_create.append(ss)
            if ss_for_create:
                StreamSchedule.objects.bulk_create(ss_for_create)
            return Response(data={"detail":"Session Scheduled for Available Time Slot Successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Test(ViewSet):
    queryset = Test.objects.all()
    permission_classes = (IsStudentAuthenticated,)
    serializer_class = TestStatusSerializer

    # Call from Student on Test Status Tab to see tests status of him self 
    def list(self, request):
        tests = self.queryset.filter(student__user = request.user)
        if tests:
            serialize = self.serializer_class(tests, many=True)
            return Response(data={'status':serialize.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail':"No Data Exist"}, status=status.HTTP_200_OK)

    # Call from Student on Test Report Tab to see tests report dept wise 
    @action(detail=False, methods=['POST'])
    def test_reports(self, request):
        dept_code = request.data.get('code')
        tests = self.queryset.filter(student__user = request.user, assessor__department= dept_code)
        if tests:
            serialize = TestReportSerializer(tests, many=True)
            return Response(data={'reports':serialize.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail':"No Data Exist"}, status=status.HTTP_200_OK)


class StudentProfile(APIView):
    permission_classes = (IsStudentAuthenticated, )
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

    # Call from Student On PSYCH Test Complete to Submit Anwer Against PSYCH Test
    def post(self, request):
        test_ans = request.data
        test_code = test_ans.get('code',None)

        try:
            student = Student.objects.get(user=request.user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            if test_code is not None:
                test_submission = PsychTestSubmission.objects.create(
                    code=test_code, student=student, answer=test_ans.get('answer', '')
                )
                return Response(data={'detail':"Test Submitted Successfully."}, status=status.HTTP_200_OK)
            return Response(data={'detail':"Please Try Again Later."}, status=status.HTTP_400_BAD_REQUEST)
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
