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

    # list of collection related to user
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


    def retrieve(self, request, pk=None):
        availability = self.get_object(request, pk)
        if availability.exists():
            serialized = AvailabilitySerializer(availability, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("No Data", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], permission_classes=[IsAssessorAuthenticated,])
    def add_availability(self, request):
        schedules = request.data.get('schedules')
        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
            availabilities = Availability.objects.filter(assessor=assessor)
            for schedule in schedules:
                import ipdb ; ipdb.set_trace()
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

    # list of collection related to user
    @action(detail=True,methods=['GET'])
    def assessor_list(self, request, pk=None):
        query_set = self.queryset.filter(assessor_id=pk, status=1)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            availabilities = serialize.data
        else:
            availabilities = []

        streams = StreamSchedule.objects.filter(assessor_id=pk)
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


    @action(detail=True, methods=['POST'], permission_classes=[IsAssessorAuthenticated, ])
    def uploadfile(self, request):
        user = request.user
        assessor = Assessor.objects.get(user=user)
        import ipdb ; ipdb.set_trace()
        # data = request.data
        # data['assessor'] = assessor
        try:
            serializer = self.serializer_class(data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
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
    permission_classes = [IsAuthenticated,]
    serializer_classes = AssessorSerializer

    def get (self, request):
        user = request.user
        try:
            assessor = Assessor.objects.get(user=user)
            serialize = self.serializer_classes(assessor)

            return  Response(data=serialize.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_401_UNAUTHORIZED)
