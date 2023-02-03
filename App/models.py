"""
*************************************
        Imported Packages
*************************************
"""

# By Default
from enum import unique
from django.db import models

# Custom User
from django.contrib.auth.models import AbstractUser, AnonymousUser

# Import UserManager Model
from App.UserManager import UserManager

# JWT
from rest_framework_simplejwt.tokens import RefreshToken

# Translations
from django.utils.translation import gettext_lazy as _


"""
**************************************************************************
                            Create Your models here
**************************************************************************
"""


"""
*************************************
        Custom User Models
*************************************
"""


AUTH_PROVIDERS = {'email': 'email'}


# Custom User
class User(AbstractUser):

    # Personal Details
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_images = models.ImageField(upload_to='user_profile', null=True,
                                       blank=True, max_length=100)

    # Authentication
    username = models.CharField(max_length=50, unique=True,
                                null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True,
                              null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    # Offical
    department = models.CharField(max_length=50, null=True, blank=True)
    enrollment_number = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=[(
        "Student", "Student"), ("Admin", "Admin"), ("Faculty", "Faculty"), ], default="Student")

    # Location
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)

    # Auth Provide
    auth_provider = models.CharField(max_length=255, blank=False, null=False,
                                     default=AUTH_PROVIDERS.get('email'))

    # Verify Account
    is_active = models.BooleanField(default=True)

    # Admin
    is_staff = models.BooleanField(default=False)

    # Imp Fields
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)

    # Images

    # Username & Required Fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone", 'username']

    # Import Module of UserMagers.py
    objects = UserManager()

    def __unicode__(self):
        return self.id

    def __str__(self):
        name = (f"{self.username} {self.phone}")
        return (name)
        # return f'{self.review_category} ({self.review_question})'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


"""
**************************************************************************
                                Management
**************************************************************************
"""


"""
*************************************
        Device & System  Log
*************************************
"""


class SystemAndDeviceLog(models.Model):
    user_idSysLog = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_query_name='SDLUserID',
                                      limit_choices_to={
                                          'is_active': True, },
                                      null=True, blank=True)

    date_time = models.DateTimeField(auto_now_add=True)

    # os - Windows or linux
    os_type = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=100, null=True, blank=True)

    # device = device id
    device_id = models.CharField(max_length=100, null=True, blank=True)

    # device type = android / ios
    device_type = models.CharField(max_length=100, default="None", choices=[
                                   ("android", "android"), ("ios", "ios"), ("None", "None"), ])

    # FCM
    fcm_token = models.CharField(max_length=200, null=True, blank=True)
    active_fcm = models.BooleanField(default=True)

    browser = models.CharField(max_length=100, null=True, blank=True)
    brower_version = models.CharField(max_length=100, null=True, blank=True)


"""
****************************************************************************************************************************************************
                                                                CLB - Review 
****************************************************************************************************************************************************
"""


"""
*******************
    CLB Review 
*******************
"""


class Review(models.Model):
    Review_Answer = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]

    review_answer = models.IntegerField(choices=Review_Answer, default=0)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    Review_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_query_name='ReviewUserID',
                                  limit_choices_to={
                                      'is_active': True, },
                                  null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)


"""
*******************
    FAQ Model
*******************
"""


class FAQ(models.Model):

    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.question}"


"""
****************************************************************************************************************************************************
                                                            Notification
****************************************************************************************************************************************************
"""


class Notification(models.Model):

    usersType = models.CharField(max_length=50, choices=[("All", "All"), ("Student", "Student"),
                                                         ("Admin", "Admin"), ("Faculty", "Faculty"), ], default="All")
    title = models.CharField(max_length=100, blank=True, null=True,)
    body = models.TextField(max_length=251, blank=True, null=True,)

    Notif_image = models.ImageField(
        upload_to="Notification", blank=True, null=True, )

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)


"""
*************************************
        Verify Email & Mobile 
*************************************
"""


class Verify_Email_OTP(models.Model):

    email = models.EmailField(max_length=254)
    is_verify_email = models.BooleanField(default=False)

    otp = models.CharField(max_length=7, null=True, blank=True)
    gen_datetime = models.DateTimeField(auto_now_add=True)
    exp_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


"""
*************************************
       Location
*************************************
"""


class Location(models.Model):

    location_area = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location_area} - {self.landmark}"


"""
*************************************

*************************************
"""


class proposal_trip(models.Model):

    date_time = models.DateTimeField(auto_now_add=True)

    proposal_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name="PorposalUser",
                                      related_query_name="PorposalUserQuery",
                                      limit_choices_to={"is_active": True}, null=True, blank=True)

    from_location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                      related_name="UserFromLocation",
                                      related_query_name="UserFromLocationQUery",
                                      limit_choices_to={"is_active": True})

    to_location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                    related_name="UserToLocation",
                                    related_query_name="UserToLocationQUery",
                                    limit_choices_to={"is_active": True})

    vehical_type = models.CharField(max_length=50, choices=[("Car", "Car"), ("Bike", "Bike"), ],
                                    default="Bike")
    vehical_number = models.CharField(max_length=50, )

    seat_availability = models.IntegerField(choices=[(1, 1),
                                                     (2, 2), (3, 3), (4, 4)], default=1)

    is_cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.proposal_user} {self.seat_availability} "


class take_trip(models.Model):

    date_time = models.DateTimeField(auto_now_add=True)

    rider_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="TakerUser",
                                   related_query_name="TakerUserQuery",
                                   limit_choices_to={"is_active": True}, null=True, blank=True)

    from_location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                      related_name="RiderFromLocation",
                                      related_query_name="RiderFromLocationQuery",
                                      limit_choices_to={"is_active": True})

    to_location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                    related_name="RiderToLocation",
                                    related_query_name="RiderToLocationQuery",
                                    limit_choices_to={"is_active": True})

    proposal_seat = models.IntegerField(choices=[(1, 1),
                                                 (2, 2), (3, 3), (4, 4)])
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rider_user} {self.date_time}"
