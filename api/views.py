import random
import uuid
import datetime
from django.shortcuts import render
from django.db.models import Q, Avg, Sum
from django.core.mail import EmailMessage

from rest_framework.views import  APIView
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from api.models import User, Role, CurrentAffair, FreeTest, HeaderImage
from student.models import Student, Address, PostOffice, StreamSchedule
from api.permissions import IsStudentAuthenticated
from api.serializers import CurrentAffairSerializer, HeaderImageSerializer


class Signup(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Create Student.
        """
        try:
            validated_data =  request.data

            # 1. User Create
            user = dict(
                username=validated_data.get('username'),
                password=validated_data.get('password'),
                email=validated_data.get('email'),
            )

            user, _ = User.objects.get_or_create(**user)
            user.role = Role.STUDENT
            user.save()

            # 2. Address Create
            address = dict(
                flat_block=validated_data.get('flat'),
                street=validated_data.get('street'),
                area=validated_data.get('area'),
                phone=validated_data.get('phone'),
                post_office=PostOffice.objects.get(
                    id=int(validated_data.get('postoffice'))
                )
            )

            address, _ = Address.objects.get_or_create(**address)

            print(validated_data.get('profile'))
            # 3. Student Create
            student = dict(
                    user = user,
                    first_name = validated_data.get('firstname'),
                    middle_name = validated_data.get('middlename'),
                    last_name = validated_data.get('lastname'),
                    gender = validated_data.get('gender'),
                    dob = validated_data.get('dob'),
                    occupation_id = validated_data.get('occupation'),
                    marital_status = validated_data.get('marital'),
                    mobile = validated_data.get('mobile'),
                    address = address,
                    security_question_id = validated_data.get('squestion'),
                    security_answer = validated_data.get('sanswer'),
                    plan = validated_data.get('plan', 1),
                    image=validated_data.get('profile')
            )

            student, _ = Student.objects.get_or_create(**student)

            # 4. Token Create
            token, _ = Token.objects.get_or_create(user=user)
            
            response = {
                "token":token.key,
                "role":Role.STUDENT,
                "user_id":token.user_id
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for LogIn Student.
        """
        try:
            data = request.data
            

            username =str(data.get('username'))
            password =str(data.get('password'))
            # import ipdb ; ipdb.set_trace()
            print(username)
            print(password)
            if not User.objects.filter((
                Q(email=username) | Q(username=username)
                )).exists():
                return Response(data={'reason':'Username Not Found.'}, status=status.HTTP_403_BAD_REQUEST)
            else:
                user = User.objects.filter((
                    Q(email=username) | Q(username=username)
                ),
                password=password)
                if not user:
                    return Response(data={'reason':'Password is Not Matched.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    token, _ = Token.objects.get_or_create(user=user.last())
                    response = {
                        'access_token': str(token.key),
                        'role':user.last().role,
                        'user_id': str(token.user_id)
                    }
                return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPassword(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        try:
            input_email = request.data.get('email','')
            # user = User.objects.filter(email=input_email)
            # if user.exists():
            if input_email:
                subject = "Reset Password Link"
                link = 'http://localhost:3000/reset_password/' + str(uuid.uuid4()) + "/1"
                body = "Hi,\n Please find link.\n" + link + "\n\nThanks & Regards\n Army"
                email = EmailMessage(subject=subject, body=body, to=('shubhampratapcool13@gmail.com',))
                try:
                    email.send()
                    return Response(data={'detail':"Link has been sent to email.Please check."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(data={'error':e}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'details':"There is no email."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPassword(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Reset Password.
        """
        password = str(request.data.get('pwd'))
        confirm_password = str(request.data.get('cnfrm_pwd'))
        user_id = int(request.data.get('id'))
        user = User.objects.filter(id=user_id)
        if user.exists():
            user.update(password=password)
            return Response(data={'detail':"Password Has Been Changed."}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'detail':"Please Try Again."}, status=status.HTTP_304_NOT_MODIFIED)


class LogOut(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, format=None):
        try:
            Token.objects.filter(user=request.user).delete()
            return Response(data={'detail':"User logged out."},status=status.HTTP_200_OK)
        except  Exception as e:
            return Response(data={'error':e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Plan(APIView):
    permission_classes = (IsStudentAuthenticated,)

    def post(self,request, format=None):
        plan = str(request.data.get('plan'))
        try:
            student = Student.objects.filter(user=request.user)
            if student.exists():
                student.update(plan=int(plan))
                return Response(data={'detail':"Plan Updated"}, status=status.HTTP_200_OK)
            else:
                return Response(data={'detail':"User Not Find"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendOTP(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        email = request.data.get('email','')
        otp = random.randint(1000,9999)

        if email:
            is_exam_taken = FreeTest.objects.filter(email= email)
            if is_exam_taken:
                return Response(data={'detail':"Already Exam Taken."}, status=status.HTTP_202_ACCEPTED)
            subject = "OTP To Enter Into Test"
            body = "Hi,\n Here is your requested otp: \n  {} \n\nThanks & Regards\n Army".format((otp))
            Email = EmailMessage(subject=subject, body=body, to=(email,))
            try:
                Email.send()
                f = FreeTest.objects.create(email=email)
                return Response(data={'detail':"OTP has been sent to email.Please check.", "OTP":otp}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'details':"There is no email."}, status=status.HTTP_400_BAD_REQUEST)


class CurrentAffairView(APIView):
    permission_classes = [AllowAny, ]
    serializer_classes = CurrentAffairSerializer

    def get(self, request, cat):
        user = request.user
        category = str(cat)
        response = {}

        ca = CurrentAffair.objects.filter(
            category=category
        )
        if ca.exists():
            serialize = self.serializer_classes(ca, many=True)
            response.update({
                'is_exist':True,
                'ca': serialize.data
            })
        else:
            response.update({
                'is_exist':False,
                'ca': []
            })
        return  Response(data=response, status=status.HTTP_200_OK)

class HeaderImagesView(APIView):
    permission_classes = [AllowAny, ]
    serializer_classes = HeaderImageSerializer

    def get(self, request):
        response = {}

        images = HeaderImage.objects.all()
        if images.exists():
            serialize = self.serializer_classes(images, many=True)
            response.update({
                'is_exist':True,
                'images': serialize.data
            })
        else:
            response.update({
                'is_exist':False,
                'images': []
            })
        return  Response(data=response, status=status.HTTP_200_OK)


class AssessorStar(APIView):
    permission_classes = [AllowAny, ]
    serializer_classes = CurrentAffairSerializer

    def get(self, request):
        response = {
            'is_exist': False,
            'assessor': [],
            'assessors': []
        }

        assessor = StreamSchedule.objects.filter(
            start_time__date=datetime.datetime.today()
        ).values(
            'assessor__first_name', 'assessor__last_name', 'assessor__user__email', 'assessor__image'
        ).annotate(Avg('rating')).order_by('rating__avg')

        assessors = StreamSchedule.objects.values(
            'assessor__first_name', 'assessor__last_name', 'assessor__user__email', 'assessor__image'
        ).annotate(Avg('rating')).order_by('rating__avg')

        if assessor.exists():
            response.update({
                'is_exist':True,
                'assessor': list(assessor)[:1]
            })
        if assessors.exists():
            response.update({
                'is_exist':True,
                'assessors': list(assessors)[:3]
            })

        return  Response(data=response, status=status.HTTP_200_OK)
