from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action


from student.models import State, City, Pincode, PostOffice, TestSchedule, Test
from student.serializers import  StateSerializer, CitySerializer, PincodeSerializer, PostofficeSerializer, TestScheduleSerializer


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


class TestScheduleViewSet(ViewSet):
    queryset = TestSchedule.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TestScheduleSerializer

    def get_object(self, request, id):
        testschedule = self.queryset.filter(id=id)
        return testschedule

    # list of collection related to user
    @action(detail=True,methods=['GET'])
    def student_list(self, request, pk=None):
        query_set = self.queryset.filter(student_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            testschedules = serialize.data
            is_success = True
        else:
            testschedules = None
            is_success = False

        context = {
            "is_success": is_success,
            "testschedules": testschedules
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(detail=True,methods=['GET'])
    def assessor_list(self, request, pk=None):
        query_set = self.queryset.filter(assessor_id=pk)
        if query_set.exists():
            serialize = self.serializer_class(query_set, many=True)
            testschedules = serialize.data
            is_success = True
        else:
            testschedules = None
            is_success = False

        context = {
            "is_success": is_success,
            "testschedules": testschedules
        }
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        testschedule = self.get_object(request, pk)
        if testschedule.exists():
            serialized = TestScheduleSerializer(testschedule, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("No Data.", status=status.HTTP_404_NOT_FOUND)
