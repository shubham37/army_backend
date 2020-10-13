from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from assessor.models import Availability, Briefcase
from assessor.serializers import AvailabilitySerializer, BriefcaseSerializer


class AvailabilityViewSet(ViewSet):
    queryset = Availability.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AvailabilitySerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            availability = serialize.data
            is_success = True
        else:
            availability = None
            is_success = False

        context = {
            "is_success": is_success,
            "availability": availability
        }
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        availability = self.get_object(request, pk)
        if availability.exists():
            serialized = AvailabilitySerializer(availability, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("No Data", status=status.HTTP_404_NOT_FOUND)

    # list of collection related to user
    @action(detail=True,methods=['GET'])
    def assessor_list(self, request, pk=None):
        query_set = self.queryset.filter(assessor_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            availabilities = serialize.data
            is_success = True
        else:
            availabilities = None
            is_success = False

        context = {
            "is_success": is_success,
            "availabilities": availabilities
        }
        return Response(context, status=status.HTTP_200_OK)


class BriefcaseViewSet(ViewSet):
    queryset = Briefcase.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BriefcaseSerializer

    def get_object(self, request, id):
        briefcase = self.queryset.filter(id=id)
        return briefcase

    # list of collection related to user
    def list(self, request):
        query_set = self.queryset
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
