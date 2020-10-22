import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from assessor.models import Availability, Briefcase, Assessor
from assessor.serializers import AvailabilitySerializer, BriefcaseSerializer, \
    AssessorSerializer
from api.permissions import IsAssessorAuthenticated

from student.models import StreamSchedule
from student.serializers import StreamScheduleSerializer

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
                return Response(data={"detail":"Record Deleted Successfully."}, status=status.HTTP_200_OK)            
            return Response(data={"detail":"Record is not Exist."}, status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(data={"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Call from Assessor on Schedule For Today Tab to list of today availabilities and streamSchedules
    @action(detail=False, methods=['GET'], permission_classes=[IsAssessorAuthenticated,])
    def today(self, request):
        today = datetime.datetime.today()
        # query_set = self.queryset.filter(assessor__user=request.user, status=1, start_time__date=today)
        # if query_set.exists():
        #     serialize = self.serializer_class(query_set, many=True)
        #     availabilities = serialize.data
        # else:
        #     availabilities = []

        streams = StreamSchedule.objects.filter(assessor__user=request.user, start_time__date=today)
        if streams.exists():
            serialize = StreamScheduleSerializer(streams, many=True)
            not_availabilities = serialize.data
        else:
            not_availabilities = []

        context = {
            # "availabilities": availabilities,
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
        assessor = Assessor.objects.get(user=user)
        data = request.data
        data['assessor_id'] = assessor.id
        try:
            if '.mp4' in data.get('file_name') or '.avi' in  data.get('file_name'):
                data.update({'file_type':1})
            elif '.doc' in data.get('file_name') or '.docs' in  data.get('file_name'):
                data.update({'file_type':2})
            elif '.jpeg' in data.get('file_name') or '.png' in  data.get('file_name'):
                data.update({'file_type':3})

            br = Briefcase.objects.create(**data)
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
    permission_classes = [IsAuthenticated, ]
    serializer_classes = AssessorSerializer

    def get(self, request, dep):
        user = request.user
        dept_code = str(dep)
        response = {}

        assessors = Assessor.objects.filter(
            department=dept_code
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
