"""
*************************************
        Imported Packages
*************************************
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


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

    # Verify OTp
    Verify_Email_OTP,

    # Location
    Location,

    # Rider
    proposal_trip,
    take_trip

)


"""
**************************************************************************
                                Set Up Admin
**************************************************************************
"""


"""
*************
    User
*************
"""


# User Admin
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'first_name', 'enrollment_number', 'department',
                    'email', 'is_active', 'user_type']

    # list_filter = ['is_active', 'is_staff', ]

    readonly_fields = ["id", "created_on",
                       "updated_on", "created_by", "updated_by"]

    fieldsets = (
        ("Register Info:", {"fields": ("id", "email",
         "username",  "phone", "password")}),
        ("Personal Info", {
         "fields": ("first_name", "last_name", "profile_images"), },),
        ("Offical", {"fields": ("department",
         "enrollment_number", "user_type"), },),
        ("Location", {"fields": ("latitude", "longitude"), },),
        ("Other Info", {"fields": ("auth_provider",), },),
        ("Login Info", {"fields": ("last_login",), },),
        ("Time Stamp Info", {"fields": ("created_on",
         "created_by", "updated_on", "updated_by"), },),
        ("Permissions", {"fields": ("user_permissions", "groups"), },),
        ("Admin Login", {"fields": ("is_active", "is_superuser",
         "is_staff", ), },),
    )


"""
*************
    SystemAndDeviceLog
*************
"""


@admin.register(SystemAndDeviceLog)
class SystemAndDeviceLog_Admin(admin.ModelAdmin):
    list_display = ["id", "user_idSysLog", "device_type", "active_fcm"]

    readonly_fields = ["id", "date_time"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Active Log   Details:", {"fields": ("user_idSysLog", "date_time", "os_type",
         "os_version", "device_type", "device_id", "browser", "brower_version", "fcm_token", "active_fcm")},),
    )


"""
*************
    CLB - Review 
*************
"""


@admin.register(Review)
class Review_Admin(admin.ModelAdmin):
    list_display = ["id", "review_answer", "Review_by"]

    readonly_fields = ["id", "created_on"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Rating:", {"fields": ("review_answer",)},),
        ("Comment:", {"fields": ("Review_by", "comment")},),
        ("TimeStamp ", {"fields": ("created_on",), },),
    )


"""
*******************
    FAQ 
*******************
"""


@admin.register(FAQ)
class FAQ_Admin(admin.ModelAdmin):
    list_display = ["id", "question", "answer", "is_active"]

    readonly_fields = ["id", "created_on",
                       "updated_on", "created_by", "updated_by"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("FAQ:", {"fields": ("question", "answer",)},),
        ("Active ", {"fields": ("is_active",), },),
        ("Time Stamp Info", {"fields": ("created_on",
         "created_by", "updated_on", "updated_by"), },),
    )


"""
*******************
    Notification
*******************
"""


@admin.register(Notification)
class Notification_Admin(admin.ModelAdmin):
    list_display = ["id", "title",  "is_active"]

    readonly_fields = ["id",  "created_on",
                       "updated_on", "created_by", "updated_by"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Notification:", {
         "fields": ("usersType", "title", "body", "Notif_image", )},),
        ("Active ", {"fields": ("is_active",), },),
        ("Time Stamp Info", {"fields": ("created_on",
         "created_by", "updated_on", "updated_by"), },),
    )


"""
*************
     Verify Email & Mobile 
*************
"""


@admin.register(Verify_Email_OTP)
class Verify_Email_OTP_Admin(admin.ModelAdmin):
    list_display = ["id", "email", "is_verify_email", "otp",
                    ]

    readonly_fields = ["id", "gen_datetime"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),

        ("Email:", {"fields": ("email", "is_verify_email",)},),
        ("OTP:", {"fields": ("otp", "gen_datetime", "exp_datetime",)},),

    )


"""
*************
     Location
*************
"""


@admin.register(Location)
class Location_Admin(admin.ModelAdmin):
    list_display = ["id", "location_area", "landmark", "is_active",
                    ]

    readonly_fields = ["id", ]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Email:", {"fields": ("location_area", "landmark",)},),
        ("Active:", {"fields": ("is_active", )},),
    )


"""
*************
     proposal_trip
*************
"""


@admin.register(proposal_trip)
class proposal_trip_Admin(admin.ModelAdmin):
    list_display = ["id", "date_time", "proposal_user", "from_location", "to_location", "is_cancel"
                    ]

    readonly_fields = ["id", ]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Date:", {"fields": ("date_time", )},),
        ("User:", {"fields": ("proposal_user", )},),

        ("Location:", {"fields": ("from_location", "to_location")},),
        ("vehical:", {"fields": ("vehical_type",
         "vehical_number", "seat_availability")},),

        ("Active:", {"fields": ("is_cancel", )},),
    )


@admin.register(take_trip)
class take_trip_Admin(admin.ModelAdmin):
    list_display = ["id", "date_time", "rider_user",
                    "from_location", "to_location", ]

    readonly_fields = ["id", "date_time"]

    fieldsets = (
        # Id Informations
        ("Registry:", {"fields": ("id",)},),
        ("Date:", {"fields": ("date_time", )},),
        ("User:", {"fields": ("rider_user", )},),

        ("Location:", {"fields": ("from_location", "to_location")},),
        ("Proposal:", {"fields": ("proposal_seat", )},),

        ("Active:", {"fields": ("is_complete", "is_deleted")},),
    )
