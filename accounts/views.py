from django.shortcuts import render
from rest_framework.views import  APIView
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from  django.contrib.auth.models import  User


class Signup(APIView):

    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        """
            Api for Create Student.
        """
        import ipdb; ipdb.set_trace()
        return Response(data=None, status=status.HTTP_201_CREATED)


class Login(APIView):

    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        """
            Api for LogIn Student.
        """
        return Response(data=None, status=status.HTTP_200_OK)


class ForgotPassword(APIView):

    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        return Response(data=None, status=status.HTTP_200_OK)


class ResetPassword(APIView):

    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        """
            Api for Reset Password.
        """
        return Response(data=None, status=status.HTTP_205_RESET_CONTENT)
