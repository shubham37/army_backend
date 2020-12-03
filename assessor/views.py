import datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from assessor.models import Availability, Briefcase, Assessor, Department, Position
from assessor.serializers import AvailabilitySerializer, BriefcaseSerializer, \
    AssessorSerializer, DepartmentSerializer, PositionSerializer
from api.permissions import IsAssessorAuthenticated

from student.models import StreamSchedule, Instruction, \
    TestSubmission, ProgressReport, Student
from student.serializers import StreamScheduleSerializer, \
    InstructionSerializer, ProgressReportSerializer, \
        TestSubmissionSerializer, StudentSerializer


class AvailabilityViewSet(ViewSet):
    queryset = Availability.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AvailabilitySerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability

    # Call from Assessor on Training Schedule Tab to list of availabilities and streamSchedules
    def list(self, request):
        query_set = self.queryset.filter(assessor__user=request.user, status=1)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            availabilities = serialize.data
        else:
            availabilities = []

        streams = StreamSchedule.objects.filter(assessor__user=request.user)
        if streams.exists():
            serialize = StreamScheduleSerializer(streams, many=True)
            not_availabilities = serialize.data
        else:
            not_availabilities = []

        context = {
            "availabilities": availabilities,
            "not_availabilities": not_availabilities
        }
        return Response(context, status=status.HTTP_200_OK)

    # Call from Assessor on Training Schedule Tab to Add New or Update older one
    @action(detail=False, methods=['POST'], permission_classes=[IsAssessorAuthenticated,])
    def add_availability(self, request):
        schedules = request.data.get('schedules')
        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
            availabilities = Availability.objects.filter(assessor=assessor)
            data_for_create = []
            for schedule in schedules:
                print(schedule.get('Id'))
                availability = availabilities.filter(id=schedule.get('Id'))
                if availability.exists():
                    availability.update(
                        status = schedule.get('status',1),
                        start_time = datetime.datetime.strptime(schedule.get('StartTime'), '%Y-%m-%dT%H:%M:%S.%fz'),
                        end_time = datetime.datetime.strptime(schedule.get('EndTime'), '%Y-%m-%dT%H:%M:%S.%fz')
                    )
                else:
                    data_for_create.append(
                        Availability(
                            assessor=assessor,
                            status = schedule.get('status',1),
                            start_time = datetime.datetime.strptime(schedule.get('StartTime'), '%Y-%m-%dT%H:%M:%S.%fz'),
                            end_time = datetime.datetime.strptime(schedule.get('EndTime'), '%Y-%m-%dT%H:%M:%S.%fz')
                        )
                    )
            if data_for_create:
                try:
                    Availability.objects.bulk_create(data_for_create)
                    return Response(data={"detail":"Data Created and Updated Successfully."}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error":"Updated but not created"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data={"detail":"Data Updated Successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(data={"error":e}, status=status.HTTP_304_NOT_MODIFIED)

    # Call from Assessor on Training Schedule Tab to Delete one
    @action(detail=False, methods=['POST'], permission_classes=[IsAssessorAuthenticated,])
    def delete_availabilities(self, request):
        schedules = request.data.get('schedules_ids')
        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
            availabilities = Availability.objects.filter(assessor=assessor, id__in=schedules)
            if availabilities.exists():
                availabilities.delete()
                return Response(data={'is_delete':True,"detail":"Record Deleted Successfully."}, status=status.HTTP_200_OK)            
            return Response(data={'is_delete':False,"detail":"Record is not Exist."}, status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(data={"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Call from Assessor on Schedule For Today Tab to list of today availabilities and streamSchedules
    @action(detail=False, methods=['GET'], permission_classes=[IsAssessorAuthenticated,])
    def today(self, request):
        today = datetime.datetime.today()
        streams = StreamSchedule.objects.filter(assessor__user=request.user, start_time__date=today)
        if streams.exists():
            serialize = StreamScheduleSerializer(streams, many=True)
            not_availabilities = serialize.data
        else:
            not_availabilities = []

        context = {
            "schedules": not_availabilities
        }
        return Response(context, status=status.HTTP_200_OK)

    # Call from Student on Dept wise Assessor Availability Tab to list of availability
    @action(detail=False,methods=['POST'])
    def assessor_dept_list(self, request):
        query_set = self.queryset.filter(assessor_id=request.data.get('assessor'), status=1)
        availabilities = []
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            availabilities = serialize.data
        context = {
            "availabilities": availabilities
        }
        return Response(data=context, status=status.HTTP_200_OK)


class BriefcaseViewSet(ViewSet):
    queryset = Briefcase.objects.all()
    permission_classes = (IsAssessorAuthenticated,)
    serializer_class = BriefcaseSerializer

    def get_object(self, request, id):
        briefcase = self.queryset.filter(id=id)
        return briefcase

    # list of collection related to user
    def list(self, request):
        user = request.user
        query_set = self.queryset.filter(assessor__user=user)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            briefcases = serialize.data
            is_success = True
        else:
            briefcases = None
            is_success = False

        context = {
            "is_success": is_success,
            "briefcases": briefcases
        }
        return Response(context, status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'], permission_classes=[IsAssessorAuthenticated, ])
    def uploadfile(self, request):
        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_401_UNAUTHORIZED)
        file = request.data.get('file')
        try:
            br = Briefcase.objects.create(file=file, assessor_id=assessor.id)
            return Response(data={'detail':"Uploaded Successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        briefcase = self.get_object(request, pk)
        if briefcase.exists():
            serialized = BriefcaseSerializer(briefcase, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("No Data", status=status.HTTP_404_NOT_FOUND)

    # list of collection related to user
    @action(detail=True,methods=['GET'])
    def assessor_list(self, request, pk=None):
        query_set = self.queryset.filter(assessor_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            briefcases = serialize.data
            is_success = True
        else:
            briefcases = None
            is_success = False

        context = {
            "is_success": is_success,
            "briefcases": briefcases
        }
        return Response(context, status=status.HTTP_200_OK)


class AssessorDept(APIView):
    permission_classes = [AllowAny, ]
    serializer_classes = AssessorSerializer

    def get(self, request, dep):
        user = request.user
        dept_code = str(dep)
        response = {}

        assessors = Assessor.objects.filter(
            department__code=dept_code
        )
        if assessors.exists():
            serialize = self.serializer_classes(assessors, many=True)
            response.update({
                'is_exist':True,
                'assessors': serialize.data
            })
        else:
            response.update({
                'is_exist':False,
                'assessors': []
            })
        return  Response(data=response, status=status.HTTP_200_OK)


class AssessorProfile(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = AssessorSerializer

    def get(self, request):
        # import ipdb; ipdb.set_trace()

        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
            serialize = self.serializer_classes(assessor)

            return  Response(data=serialize.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_401_UNAUTHORIZED)


class DepartmentViewSet(ViewSet):
    queryset = Department.objects.all()
    permission_classes = (IsAssessorAuthenticated,)
    serializer_class = DepartmentSerializer

    def list(self, request):
        if  self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Department Found."}, status=status.HTTP_200_OK)


class PositionViewSet(ViewSet):
    queryset = Position.objects.all()
    permission_classes = (IsAssessorAuthenticated,)
    serializer_class = PositionSerializer

    def list(self, request):
        if  self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Position Found."}, status=status.HTTP_200_OK)


class AssessorInstruction(ViewSet):
    queryset = Instruction.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = InstructionSerializer

    # Call from Assessor to see Instruction who has training shcedule with them.
    def list(self, request):
        # import ipdb; ipdb.set_trace()
        user = request.user
        instructions = self.queryset.filter(assessor__user=user)
        if instructions:
            serialize = self.serializer_class(instructions.last())
            return Response(data={'is_success':True, 'instruction': serialize.data}, status=status.HTTP_200_OK)
        return Response(data={'is_success':False, 'detail': "No Data Found."}, status=status.HTTP_200_OK)

    # Call from Assessor to update Instruction who has training shcedule with them.
    @action(detail=False, methods=['POST'])
    def add_update(self, request):
        instruction_id = request.data.get('id', None)
        assessor = request.user
        instruction = request.data.get('instruction', '')
        if instruction_id is not None:
            d = self.queryset.filter(id=instruction_id)
            d.update(instruction=str(instruction))
        else:
            ins = Instruction.objects.create(assessor=assessor, instruction=instruction)
        return Response(data={'detail': "Done."}, status=status.HTTP_200_OK)

    # Call from Student to See Instruction Which is given by Assessor
    @action(detail=False, methods=['GET'])
    def student_list(self, request):
        assessors = set(StreamSchedule.objects.filter(student__user=request.user).values_list('assessor_id'))
        instructions = self.queryset.filter(assessor_id__in=assessors)
        if instructions.exists():
            serialize = self.serializer_class(instructions, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Data Found."}, status=status.HTTP_200_OK)


class TestChecking(ViewSet):
    queryset = TestSubmission.objects.all()
    serializer_class = TestSubmissionSerializer
    permission_classes = [IsAuthenticated,]

    # Call from Assessor on Test Report Tab to see tests 
    def list(self, request):
        assessor = Assessor.objects.get(user=request.user)
        students = StreamSchedule.objects.filter(assessor=assessor).values_list('student_id')
        tests = self.queryset.filter(student_id__in=students,submission_status=2, checking_status=1)
        if tests:
            serialize = self.serializer_class(tests, many=True)
            return Response(data={'is_data':True, 'tests':serialize.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'is_data':False, 'detail':"No Data Exist"}, status=status.HTTP_200_OK)
        

    # Call from Assessor on Test Report Tab to update his assessmet on tests report
    @action(detail=False, methods=['Post'])
    def update_reports(self, request):
        data = request.data # remarks and comment and id
        # import ipdb; ipdb.set_trace()
        assessor = Assessor.objects.get(user=request.user)
        tests = self.queryset.filter(id = data.get('id'))
        if tests.exists():
            tests.update(
                remark =data.get('remark'),
                comment =data.get('comment'),
                checking_status = 2,
                assessor =assessor
            )
            return Response(data={'is_update':True}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(data={'is_update':False}, status=status.HTTP_200_OK)


class ProgressReports(ViewSet):
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    permission_classes = [IsAuthenticated,]

    # Call from Assessor on Progress Report Tab to see report to update
    def list(self, request):
        assessor = Assessor.objects.get(user=request.user)
        students = StreamSchedule.objects.filter(assessor=assessor, status=2).values_list('student')
        reports =self.queryset.filter(student__in=students)
        if reports:
            serialize = self.serializer_class(reports, many=True)
            return Response(data={'is_data':True, 'reports':serialize.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'is_data':False, 'detail':"No Data Exist"}, status=status.HTTP_200_OK)
        

    # Call from Assessor on Test Report Tab to update his assessmet on tests report
    @action(detail=False, methods=['Post'])
    def update_progress(self, request):
        data = request.data # remarks and comment and id
        assessor = Assessor.objects.get(user=request.user)
        progress_reports = self.queryset.filter(id = data.get('id'))
        if progress_reports.exists():
            progress_reports.update(
                report =data.get('report'),
                assessor =assessor
            )
            return Response(data={'is_update':True}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(data={'is_update':False}, status=status.HTTP_200_OK)


class Rating(ViewSet):
    queryset = StreamSchedule.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = StreamScheduleSerializer

    def list(self, request):
        ratings = self.queryset.filter(assessor__user=request.user)
        if ratings.exists():
            data = {
                'ZERO': ratings.filter(rating=0).count(),
                'ONE': ratings.filter(rating=1).count(),
                'TWO': ratings.filter(rating=2).count(),
                'THREE': ratings.filter(rating=3).count(),
                'FOUR': ratings.filter(rating=4).count(),
                'FIVE': ratings.filter(rating=5).count()
            }
            # serialize = self.serializer_class(ratings, many=True)
            return Response(data={'is_data':True,"ratings": data}, status=status.HTTP_200_OK)
        return Response(data={'is_data':False,'detail': "No Data Found."}, status=status.HTTP_200_OK)
