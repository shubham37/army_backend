from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAdminAuthenticated
from api.models import User
from admin_user.serializers import AdminSerializer


class  AdminProfile(APIView):
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = AdminSerializer

    def get(self, request):
        try:
            admin_user=request.user
        except Exception as e:
            return Response(data={'detail':e},status=status.HTTP_401_UNAUTHORIZED)

        serialize = self.serializer_class(admin_user)
        return Response(data=serialize.data, status=status.HTTP_200_OK)
