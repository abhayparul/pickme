"""
*********
Rest Framework
*********
"""

# Permission
from tkinter.tix import Tree
from turtle import Turtle
from rest_framework import permissions

# Response
from rest_framework.response import Response

# Class - Generic
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.views import APIView

# Parser & Status
from rest_framework.parsers import MultiPartParser
from rest_framework import status

# Language Translation
from django.utils.translation import gettext_lazy as _

# Serializers
from rest_framework.serializers import Serializer

# Error handling
from rest_framework.exceptions import NotFound

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Json Web Token
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Email for verification
from App.EmailConfig import SendEmail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import get_template

# Forget Password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)

# Search & Filter
from rest_framework.filters import SearchFilter
import django_filters

# Custom Permission
from App import CustomPermission

from django.conf import settings

# Error - Logging
from App.Error_Log import Error_Log

# JSON Renderer For Encrypt Decrypt
from rest_framework.renderers import JSONRenderer

# Q Object
from django.db.models import Q
from django.db.models import F, Sum, Avg, Count

# Other
from django.http import HttpResponsePermanentRedirect
from django.http import Http404

# Data Time
import datetime

# Custom Function Gen
from App.otp_generate import SendEmailForOTP

# Json
import json

# Regex
import re

# Custom Pagination
from App.MyPagination import Pagination_Page_50

# Decode JWT
from App.DecodeJWT import DecodeJWT

# AuthToken
from App.AuthToken import DecodeToken

# Other Function Generate
# from App.FunctionGen import sendPush

# Models
from App.models import (
    # Custom User Model
    User,

    # System Log
    SystemAndDeviceLog,


    # Review
    Review,

    # FAQ
    FAQ,

    # Notification
    Notification,

    # Verify OTP
    Verify_Email_OTP,

    # Location
    Location,

    # Rider
    proposal_trip,
    take_trip

)


# Admin Serializer.
from App.serializers import (

    # Sign Up User
    SignUp_User_Serializers,

    # Update user
    Update_User_Serializers,

    # Login
    User_Login_Serializers,

    # System Device Log
    SystemAndDeviceLog_Serializers,

    # Review
    Review_Serializers,

    # Faq
    faq_serializers,

    # NOtification
    Notification_Serializers,

    # Verify OTP
    Verify_Email_OTP_serializers,

    # Location
    Location_serializers,

    # Proposal
    Vehical_owner_serializers,
    taken_trip_serializers,

)


"""
**************************************************************************
                            Create Your Business Logic here
**************************************************************************
"""


"""
****************************************************************************************************************************************************************
                                                                 Admin
****************************************************************************************************************************************************************
"""


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [settings.APP_SCHEME, 'http', 'https']


"""
********************
    Register & Update User
********************
"""


class SignUp_User_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    serializer_class = SignUp_User_Serializers

    @swagger_auto_schema(tags=["User"], operation_description="User can register by themself.")
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 201,
                    "response_message": _("User has been created."),
                    "response_data": user_data, },
                    status=status.HTTP_201_CREATED)
                # return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                if serializer.errors.get('password_validation'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Invalid Password")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('password_length'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Passwords must be bewtween 6  to 20 Characters.")},
                        status=status.HTTP_400_BAD_REQUEST)
                # Exists
                elif serializer.errors.get('email_exists'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Email is already existed.")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_exists'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Phone Number already is existed.")},
                        status=status.HTTP_400_BAD_REQUEST)
                # Validation
                elif serializer.errors.get('email_validation'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Please, Enter the correct E-Mail.")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_validation'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Phone must be start with '+', and Numeric")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('Phonelength'):
                    return Response({
                        "response_code": 400,
                        "response_message": _('Phone must be bewtween 8  to 12 Characters')},
                        status=status.HTTP_400_BAD_REQUEST)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


class Update_User_Profile(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomPermission.IsOwnerAndIsSuperAdmin]
    permission_classes = [permissions.AllowAny]

    serializer_class = Update_User_Serializers
    # renderer_classes = (UserRenderer)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["User"], operation_description="User can update profile by themself.",)
    def patch(self, request, pk, format=None):
        try:
            User_ID = self.get_object(pk)

            serializer = self.serializer_class(User_ID, data=request.data,  partial=True,
                                               context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 200,
                    "response_message": _("User profile has been updated."),
                    "response_data": user_data, },
                    status=status.HTTP_200_OK)

            else:

                # Exists
                if serializer.errors.get('email_exists'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Email is already existed.")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_exists'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Phone Number already is existed.")},
                        status=status.HTTP_400_BAD_REQUEST)
                # Validation
                elif serializer.errors.get('email_validation'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Please, Enter the correct E-Mail.")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_validation'):
                    return Response({
                        "response_code": 400,
                        "response_message": _("Phone must be start with '+', and Numeric")},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('Phonelength'):
                    return Response({
                        "response_code": 400,
                        "response_message": _('Phone must be bewtween 8  to 12 Characters')},
                        status=status.HTTP_400_BAD_REQUEST)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
********************
    Login User
********************
"""


class User_Login_Views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    serializer_class = User_Login_Serializers

    @swagger_auto_schema(tags=["User Login"], operation_description="User can login with OTP. and OTP will be on register email address.",)
    def post(self, request, *args, **kwargs):
        try:

            serializer = self.serializer_class(
                data=request.data, context={"request": request})

            Verify_Email_OTP.objects.filter(
                exp_datetime__lt=datetime.datetime.now()).delete()

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                """===================== Email ====================="""

                SendEmailForOTP(email=user_data["email"], id=user_data["id"])

                return Response({
                    "response_code": 200,
                    "response_message": _("OTP has been  send on register Email."),
                    "response_data": user_data},
                    status=status.HTTP_200_OK)
            else:
                if serializer.errors.get('email_exists'):
                    return Response({"response_code": 400, "response_message": _("Email already is existed.")}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


class User_Verify_Email_OTP_Views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    serializer_class = Verify_Email_OTP_serializers

    @swagger_auto_schema(tags=["User Login"], operation_description="User should verify otp.")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            email = request.data["email"]
            otp = request.data["otpCode"]

            try:
                Check_OTP = Verify_Email_OTP.objects.filter(Q(email=email) & Q(
                    exp_datetime__gt=datetime.datetime.now()) & Q(is_verify_email=False))

                if Verify_Email_OTP.objects.filter(Q(email=email) & Q(otp=otp) & Q(exp_datetime__gt=datetime.datetime.now()) & Q(is_verify_email=False)):
                    Verify_Email_OTP.objects.filter(Q(email=email) &
                                                    Q(otp=otp)).update(is_verify_email=True)

                    user1 = User.objects.get(email=email).id
                    user = User.objects.get(id=user1)

                    return Response({
                        "response_code": 200,
                        "response_message": _("Login Successfully."),
                        "response_data": {
                            "user_id": user1,
                            "user_type": user.user_type,
                            "token": {'refresh': user.tokens()['refresh'],
                                      'access': user.tokens()['access']}
                        },
                    }, status=status.HTTP_200_OK)

                elif Verify_Email_OTP.objects.filter(Q(email=email) & Q(otp=otp) & Q(exp_datetime__gt=datetime.datetime.now()) & Q(is_verify_email=True)):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": _("Email OTP Already is verified."),
                    }, status=status.HTTP_400_BAD_REQUEST)

                elif Verify_Email_OTP.objects.filter(Q(email=email) & Q(otp=otp) & Q(exp_datetime__lt=datetime.datetime.now()) & Q(is_verify_email=False)):

                    return Response({
                        "responseCode": 400,
                        "responseMessage": _("Email OTP is expired."),
                    }, status=status.HTTP_400_BAD_REQUEST)

                elif Check_OTP:

                    for i in Check_OTP:
                        if i.otp == otp:
                            Verify_Email_OTP.objects.filter(Q(email=email) & Q(
                                otp=otp)).update(is_verify_email=True)
                        else:
                            return Response({
                                "responseCode": 400,
                                "responseMessage": _("Invalid OTP"),
                            }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                Error_Log(e)
                return Response({
                    "response_code": 400,
                    "response_message": _(e)},
                    status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({'responseCode': status.HTTP_400_BAD_REQUEST, "responseMessage": serializer.errors})


"""
********************
    System & Device Log
********************
"""


class SystemAndDeviceLog_Create_Views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    serializer_class = SystemAndDeviceLog_Serializers

    @ swagger_auto_schema(tags=["Log Details"], operation_description="This API for getting System log and Store in Database.",)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            try:
                serializer.save()
                return Response({
                    "code": 201,
                    "message": _("Log has been stored."),
                    "data": serializer.data, },
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                Error_Log(e)
                return Response({"code": 400, "message": _("Invalid OTP, Please Resend OTP ")}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"code": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


"""
********************
    Review
********************
"""


class Post_Review_Views(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = Review_Serializers

    @ swagger_auto_schema(tags=["Review"], operation_description="User can post review and comments.")
    def post(self, request, *args, **kwargs):
        try:

            serializer = self.serializer_class(
                data=request.data, context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()

                """===================== Create By & Update On ====================="""

                if "Authorization" in self.request.headers:

                    token = self.request.headers["Authorization"]
                    UserID = DecodeJWT(token)

                    Review.objects.filter(
                        id=serializer.data['id']).update(Review_by=User.objects.get(id=UserID))

                return Response({
                    "response_code": 201,
                    "response_message": _("Review is posted."),
                    "response_data": serializer.data},
                    status=status.HTTP_201_CREATED)

            else:
                if serializer.errors.get('Review'):
                    return Response({"response_code": 400, "response_message": "Review Rating between 0 to 5"}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"response_code": 400, "response_message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


class Review_by_Rating_View(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["Review"], operation_description="All Review will be gotten by Rating",)
    def get(self, request, format=None):

        # TotalData = {
        #     "Total Review": CLB_Review.objects.all().count(),
        #     "Total_Avg": CLB_Review.objects.aggregate(Avg("review_answer")),
        #     "Total_Review_by_Rating": CLB_Review.objects.values('review_answer').annotate(
        #         Review_Count=Count('review_answer'))
        # }

        return Response({"responseCode": 200,
                         'responseMessage': _("Success"),
                         'responseData': {
                             "Total Review": Review.objects.all().count(),
                             "Total_Avg": Review.objects.aggregate(Avg("review_answer")),
                             "Total_Review_by_Rating": Review.objects.values('review_answer').annotate(
                                 Review_Count=Count('review_answer'))
                         }}, status=status.HTTP_200_OK)


"""
****************
FAQ    - Create
****************
"""


class Create_FAQ_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = [permissions.AllowAny]

    serializer_class = faq_serializers
    # renderer_classes = (UserRenderer)

    @swagger_auto_schema(tags=["FAQ"], operation_description="Admin can create FAQ.",)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 201,
                    "response_message": _("FAQ has been created"),
                    "response_data": user_data},
                    status=status.HTTP_201_CREATED)
                # return Response(user_data, status=status.HTTP_201_CREATED)
            else:

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
****************
FAQ     - Update
****************
"""


class Update_FAQ_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = [permissions.AllowAny]

    serializer_class = faq_serializers

    def get_object(self, pk):
        try:
            return FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["FAQ"], operation_description="Admin can Update FAQ.",)
    def patch(self, request, pk, format=None):
        try:
            User_ID = self.get_object(pk)

            serializer = self.serializer_class(User_ID, data=request.data,  partial=True,
                                               context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 200,
                    "response_message": _("FAQ has been updated."),
                    "response_data": user_data},
                    status=status.HTTP_200_OK)

            else:

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
****************
FAQ     - Delete
****************
"""


class DeleteSoft_FAQ_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = [permissions.AllowAny]

    serializer_class = faq_serializers

    queryset = FAQ.objects.filter(is_active=True)

    def get_object(self, pk):
        try:
            return FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["FAQ"], operation_description="Soft Delete  ",)
    def delete(self, request, pk, format=None):

        # """================================================"""
        id_ForDel = self.get_object(pk)

        if id_ForDel.is_active == True:

            id_ForDel.is_active = False

            id_ForDel.save()

            return Response(
                {"responseCode": 200,
                    'responseMessage': _("Successfully Deleted")},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 400,
                    'responseMessage':  _("Already Is Deleted")},
                status=status.HTTP_400_BAD_REQUEST)


"""
****************
FAQ     - List - All
****************
"""


class List_FAQ_Views(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = faq_serializers

    @ swagger_auto_schema(tags=["FAQ"], operation_description="Get Admin User Details",)
    def get(self, request, format=None):
        data = FAQ.objects.filter(is_active=True)

        if data:
            serializer = self.serializer_class(
                data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': _("Success"),
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)


"""
****************
FAQ     - List - Single
****************
"""


class Get_FAQ_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = faq_serializers

    def get_object(self, pk):
        try:
            return FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["FAQ"], operation_description=("Every User can see FAQ.",))
    def get(self, request, pk, format=None):

        data_id = self.get_object(pk)

        if data_id.is_active == True:

            serializer = self.serializer_class(
                data_id,  context={"request": request})

            # 'responseData': encrypt_data(serializer.data)},

            return Response(
                {"responseCode": 200,
                    'responseMessage': _("Success"),
                    'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)


"""
****************************************************************
Location - Create
****************************************************************
"""


class Create_Location_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = [permissions.AllowAny]

    serializer_class = Location_serializers
    # renderer_classes = (UserRenderer)

    @swagger_auto_schema(tags=["Location"], operation_description="Admin can create Location.",)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 201,
                    "response_message": _("Location has been created"),
                    "response_data": user_data},
                    status=status.HTTP_201_CREATED)
                # return Response(user_data, status=status.HTTP_201_CREATED)
            else:

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
****************
Location - Get
****************
"""


class List_Location_Views(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = Location_serializers

    @ swagger_auto_schema(tags=["Location"], operation_description="user will get the location",)
    def get(self, request, format=None):
        data = Location.objects.filter(is_active=True)

        if data:
            serializer = self.serializer_class(
                data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': _("Success"),
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)


"""
****************************************************************
                    Owner
****************************************************************
"""


class Create_Proposal_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = Vehical_owner_serializers
    # renderer_classes = (UserRenderer)

    @swagger_auto_schema(tags=["Propasal"], operation_description="Vehical Owner give proposal to Rider",)
    def post(self, request, *args, **kwargs):
        try:

            token = self.request.headers["Authorization"]
            UserID = DecodeJWT(token)

            request.data["proposal_user"] = User.objects.get(
                id=UserID).id

            serializer = self.serializer_class(
                data=request.data, context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 201,
                    "response_message": _("Proposal has been created"),
                    "response_data": user_data},
                    status=status.HTTP_201_CREATED)
                # return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                if serializer.errors.get("to_location"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("Location does not exists."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("from_location"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("Location does not exists."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("Location"):
                    return Response({
                        "response_code": 400,
                        "response_message": _("From and To Location are same."), },
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get("Vehical"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("You should enter 'Car' , 'Bike'."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("Car"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("You Should enter max 4 seat."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("Bike"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("You Should enter max 1 seat."), },
                        status=status.HTTP_404_NOT_FOUND)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


class cancel_proposal_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = Vehical_owner_serializers

    queryset = proposal_trip.objects.filter(is_cancel=False)

    def get_object(self, pk):
        try:
            return proposal_trip.objects.get(pk=pk)
        except proposal_trip.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Propasal"], operation_description="Soft Delete  ",)
    def delete(self, request, pk, format=None):

        # """================================================"""
        id_ForDel = self.get_object(pk)

        if id_ForDel.is_cancel == False:

            id_ForDel.is_cancel = True

            id_ForDel.save()

            return Response(
                {"responseCode": 200,
                    'responseMessage': _("Successfully Deleted")},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 400,
                    'responseMessage':  _("Already Is Deleted")},
                status=status.HTTP_400_BAD_REQUEST)


class List_proposal_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = Vehical_owner_serializers

    @ swagger_auto_schema(tags=["Propasal"], operation_description="Get Admin User Details",)
    def get(self, request, format=None):
        data = proposal_trip.objects.filter(
            Q(is_cancel=False) & Q(date_time__lt=datetime.datetime.now()))

        if data:
            serializer = self.serializer_class(
                data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': _("Success"),
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)


"""
****************************************************************
                    Rider 
****************************************************************
"""


class Create_Rider_views(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = taken_trip_serializers
    # renderer_classes = (UserRenderer)

    @swagger_auto_schema(tags=["Rider"], operation_description="Vehical Owner give proposal to Rider",)
    def post(self, request, *args, **kwargs):
        try:

            token = self.request.headers["Authorization"]
            UserID = DecodeJWT(token)

            request.data["rider_user"] = User.objects.get(
                id=UserID).id

            serializer = self.serializer_class(
                data=request.data, context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 201,
                    "response_message": _("Rider has been created"),
                    "response_data": user_data},
                    status=status.HTTP_201_CREATED)
                # return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                if serializer.errors.get("to_location"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("Location does not exists."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("from_location"):
                    return Response({
                        "response_code": 404,
                        "response_message": _("Location does not exists."), },
                        status=status.HTTP_404_NOT_FOUND)

                elif serializer.errors.get("Location"):
                    return Response({
                        "response_code": 400,
                        "response_message": _("From and To Location are same."), },
                        status=status.HTTP_400_BAD_REQUEST)
                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": _(e)}, status=status.HTTP_400_BAD_REQUEST)


class delete_ride_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = taken_trip_serializers

    queryset = take_trip.objects.filter(is_deleted=False)

    def get_object(self, pk):
        try:
            return take_trip.objects.get(pk=pk)
        except take_trip.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Rider"], operation_description="Soft Delete  ",)
    def delete(self, request, pk, format=None):

        # """================================================"""
        id_ForDel = self.get_object(pk)

        if id_ForDel.is_deleted == False:

            id_ForDel.is_deleted = True

            id_ForDel.save()

            return Response(
                {"responseCode": 200,
                    'responseMessage': _("Successfully Deleted")},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 400,
                    'responseMessage':  _("Already Is Deleted")},
                status=status.HTTP_400_BAD_REQUEST)


class List_rider_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = taken_trip_serializers

    @ swagger_auto_schema(tags=["Rider"], operation_description="Get Admin User Details",)
    def get(self, request, format=None):

        token = self.request.headers["Authorization"]
        UserID = DecodeJWT(token)

        request.data["rider_user"] = User.objects.get(
            id=UserID).id

        data = take_trip.objects.filter(
            Q(is_deleted=False) & Q(date_time__lt=datetime.datetime.now()) & Q(is_complete=False) & Q(rider_user=UserID))

        if data:
            serializer = self.serializer_class(
                data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': _("Success"),
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)


class Complete_ride_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = taken_trip_serializers

    queryset = take_trip.objects.filter(is_deleted=False)

    def get_object(self, pk):
        try:
            return take_trip.objects.get(pk=pk)
        except take_trip.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Rider"], operation_description="Soft Delete  ",)
    def get(self, request, pk, format=None):

        # """================================================"""
        id_ForDel = self.get_object(pk)

        if id_ForDel.is_complete == False:

            id_ForDel.is_complete = True

            id_ForDel.save()

            return Response(
                {"responseCode": 200,
                    'responseMessage': _("Successfully Completed")},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 400,
                    'responseMessage':  _("Already Is Completed")},
                status=status.HTTP_400_BAD_REQUEST)


class List_Completed_rider_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    serializer_class = taken_trip_serializers

    @ swagger_auto_schema(tags=["Rider"], operation_description="Get Admin User Details",)
    def get(self, request, format=None):

        token = self.request.headers["Authorization"]
        UserID = DecodeJWT(token)

        # request.data["rider_user"] = User.objects.get(
        #     id=UserID).id

        data = take_trip.objects.filter(
            Q(is_deleted=False) & Q(date_time__lt=datetime.datetime.now()) & Q(is_complete=True) & Q(rider_user=UserID))

        if data:
            serializer = self.serializer_class(
                data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': _("Success"),
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': _("No Data"), },
                status=status.HTTP_404_NOT_FOUND)
