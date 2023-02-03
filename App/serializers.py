"""
*************************************
        Imported Packages 
*************************************
"""

# Serializer
from dataclasses import field
from email.policy import default
from rest_framework import serializers
from rest_framework.serializers import ValidationError

# DateTime
from datetime import datetime

# Translation
from django.utils.translation import gettext_lazy as _

# Setting.py
from django.conf import settings

# Regular Expression
import re

# Authutication
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# JSON
import json

# Gen Function
from App.FunctionGen import password_validation

# Q Object
from django.db.models import Q

# DRF Extra Field
# from drf_extra_fields.fields import Base64ImageField


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


"""
****************************************************************************************************************************************************************
                                                                 Admin
****************************************************************************************************************************************************************
"""


"""
********************
    Register User
********************
"""


class SignUp_User_Serializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, required=True,)

    password = serializers.CharField(min_length=6, max_length=50,
                                     write_only=True, required=True, style={"input_type": "password",
                                                                            "placeholder": "Password"},)

    # profile_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',  'first_name', 'last_name', 'phone',  'username', 'email', 'password', 'department', 'enrollment_number', 'user_type', 'latitude', 'longitude'
        ]

        read_only_fields = ['id']

    # Validate Data

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        phone = validated_data.get("phone")

        # Exists Data
        email_exists = User.objects.filter(email=email).exists()
        phone_exists = User.objects.filter(phone=phone).exists()

        if not password_validation(password):
            raise serializers.ValidationError({"password_validation": _(
                "Invalid Password Validation")})

        elif len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError({"password_length": _(
                "Passwords must be bewtween 6  to 20 Characters.")})

        elif email_exists:
            raise serializers.ValidationError(
                {"email_exists": _("Email is already existed.")})

        elif phone_exists:
            raise serializers.ValidationError(
                {'phone_exists': _("Phone Number is already exists.")})

        # Email Validation
        elif not re.match('^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$', email):
            raise serializers.ValidationError(
                {'email_validation': _("Please, Enter the correct E-Mail.")})

        elif not re.match('^[+][0-9]*$', phone):
            raise serializers.ValidationError(
                {"phone_validation": _("Phone must be start with '+', and Numeric")})

        # Phone Length
        elif len(phone) < 8 or len(phone) > 12:
            raise serializers.ValidationError(
                {"phone_length": _("Phone must be bewtween 8  to 12 Characters")})

        return validated_data


class Update_User_Serializers(serializers.ModelSerializer):

    # profile_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',  'first_name', 'last_name', 'phone',  'department',  'latitude', 'longitude'
        ]

        read_only_fields = ['id']


"""
**********
    End-Super Loing & Signup
**********
"""


class User_Login_Serializers(serializers.ModelSerializer):

    class Meta:

        model = Verify_Email_OTP
        fields = [
            "id",
            "email"
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        email = attrs.get("email")

        # Exists
        EmailExists = User.objects.filter(
            Q(email=email) & Q(is_active=True))

        if not EmailExists:
            raise serializers.ValidationError(
                {"email_exists": _("User does not exists.")})

        return attrs


"""
********************
    System & Device Log 
********************
"""


class SystemAndDeviceLog_Serializers(serializers.ModelSerializer):

    class Meta:

        model = SystemAndDeviceLog
        fields = ["user_idSysLog", "date_time", "os_type", "os_version",
                  "device_id", "device_type", "fcm_token", "active_fcm", "browser", "brower_version"]

        read_only_fields = ['date_time']


"""
********************
     Review 
********************
"""


class Review_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ["id", "review_answer", "comment", "Review_by", "created_on"]
        read_only_fields = ['id', "created_on", "Review_by", ]

    def validate(self, attrs):
        review_answer = attrs.get('review_answer')

        if review_answer < 1 or review_answer > 5:
            raise serializers.ValidationError(
                {"Review": "Review Rating between 0 to 5"}
            )
        return super().validate(attrs)


"""
********************
     FAQ 
********************
"""


class faq_serializers(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ["id",  "question", "answer", ]
        read_only_fields = ['id', ]


"""
********************************************************************************************************************************************
                                                            Notification
********************************************************************************************************************************************
"""


class Notification_Serializers(serializers.ModelSerializer):

    Notif_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Notification
        fields = ["id", "usersType", "title", "body", "Notif_image"]

        read_only_fields = ['id', "is_active", "created_on",
                            "created_by", "updated_on", "updated_by"]


"""
********************
    Verify Email 
********************
"""


class Verify_Email_OTP_serializers(serializers.Serializer):
    otpCode = serializers.CharField(required=True)
    email = serializers.EmailField(max_length=100)

    class META:
        fields = ["email", "otpCode"]

    def validate(self, validated_data):
        email = validated_data.get("email")
        otpCode = validated_data.get("otpCode")

        if not otpCode.isdigit():
            raise serializers.ValidationError(
                {"otp_Digit": _("OTP must be Only Numberic")})

        return validated_data


"""
********************
    Location 
********************
"""


class Location_serializers(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ["id", "location_area", "landmark"]
        read_only_fields = ['id', ]


"""
********************
    Proposal 
********************
"""


class Vehical_owner_serializers(serializers.ModelSerializer):

    class Meta:
        model = proposal_trip
        fields = ["id", "proposal_user", "from_location", "to_location",
                  "vehical_type", "vehical_number", "seat_availability"]
        read_only_fields = ['id', ]

    def validate(self, attrs):
        from_location = attrs.get("from_location")
        to_location = attrs.get("to_location")
        vehical_type = attrs.get("vehical_type")
        seat_availability = attrs.get("seat_availability")

        if from_location == to_location:
            raise serializers.ValidationError(
                {"Location": "From and To Location are same."})

        elif vehical_type not in ["Car", "Bike"]:
            raise serializers.ValidationError(
                {"Vehical": "You should enter 'Car' , 'Bike'."})

        elif vehical_type == "Car":
            if seat_availability > 4:
                raise serializers.ValidationError(
                    {"Car": "You Should enter max 4 seat."})

        elif vehical_type == "Bike":
            if seat_availability != 1:
                raise serializers.ValidationError(
                    {"Bike": "You Should enter max 1 seat."})

        return super().validate(attrs)


class taken_trip_serializers(serializers.ModelSerializer):

    class Meta:
        model = take_trip
        fields = [
            "id", "rider_user", "from_location", "to_location", "proposal_seat",
        ]
        read_only_fields = ['id', ]

    def validate(self, attrs):
        from_location = attrs.get("from_location")
        to_location = attrs.get("to_location")

        if from_location == to_location:
            raise serializers.ValidationError(
                {"Location": "From and To Location are same."})

        return super().validate(attrs)
