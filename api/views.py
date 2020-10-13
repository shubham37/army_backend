from django.shortcuts import render
from django.db.models import Q
from django.core.mail import EmailMessage

from rest_framework.views import  APIView
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from api.models import User


class Signup(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Create Student.
        """
        # data = request.data

        return Response(data=None, status=status.HTTP_201_CREATED)


class Login(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for LogIn Student.
        """

        try:
            data = request.data
            if not data.get('username',''):
                raise ValueError("Username Should Not Be Blank.")
            if not data.get('password',''):
                raise ValueError("Password Should Not Be Blank.")

            username =str(data.get('username'))
            password =str(data.get('password'))

            if not User.objects.filter((
                Q(email=username) | Q(username=username)
                )).exists():
                raise ValueError("Username Not Found.")
            else:
                user = User.objects.filter((
                    Q(email=username) | Q(username=username)
                ),
                password=password)
                if not user:
                    raise ValueError("Password is Not Matched.")
                else:
                    access = AccessToken.for_user(user.last())
                    if user.last().is_student:
                        role = 0
                    elif user.last().is_staff:
                        role = 1
                    else:
                        role = 2

                    response = {
                        'access_token': str(access.get('jti')),
                        'role':role,
                        'user_id': str(access.get('user_id'))
                    }
                return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_403_FORBIDDEN)


class ForgotPassword(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        try:
            email = request.data.get('email',None)
            if email is not None:
                subject = "Reset Password Link"
                body = "Hi,\n Please find link.\n\nThanks & Regards\n Army"
                email = EmailMessage(subject=subject, body=body, to=(email,))
                try:
                    email.send()
                    return Response(data={'detail':"Link has been sent to email.Please check."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(data={'error':e}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'details':"There is no email."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(data=None, status=status.HTTP_200_OK)


class ResetPassword(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Reset Password.
        """
        password = str(request.data.get('pwd'))
        confirm_password = str(request.data.get('cnfrm_pwd'))
        email = str(request.data.get('email'))
        if password and confirm_password and email:
            if password == confirm_password:
                user = User.objects.filter(email=email)
                if user:
                    user.update(password=password)
                    return Response(data={'detail':"Password Has Been Changed."}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data={'detail':"Please Try Again."}, status=status.HTTP_304_NOT_MODIFIED)
            else:
                return Response(data={'detail':"Password & ConfirmPassword Should Be Match."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail':"Please check details."}, status=status.HTTP_400_BAD_REQUEST)
