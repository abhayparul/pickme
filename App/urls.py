"""
*************************************
        Imported Packages 
*************************************
"""


# By Default
from django.contrib import admin
from django.urls import path, include

# App Views
from App.views import (

    # Sign Up Update User
    SignUp_User_views,
    Update_User_Profile,

    # Login
    User_Login_Views,
    User_Verify_Email_OTP_Views,

    # System Log
    SystemAndDeviceLog_Create_Views,

    # Review
    Post_Review_Views,
    Review_by_Rating_View,

    # FAQ
    Create_FAQ_views,
    Update_FAQ_views,
    DeleteSoft_FAQ_views,
    List_FAQ_Views,
    Get_FAQ_views,

    # Location
    Create_Location_views,
    List_Location_Views,

    # Proposal
    Create_Proposal_views,
    cancel_proposal_view,
    List_proposal_view,

    # Rider
    Create_Rider_views,
    delete_ride_view,
    List_rider_view,
    Complete_ride_view,
    List_Completed_rider_view,

)

"""
**************************************************************************
                            ULRS
**************************************************************************
"""

urlpatterns = [
    # User
    path("SignUp_User/", SignUp_User_views.as_view(), name="SignUpUserViews"),
    path("Update_User_profile/<int:pk>/", Update_User_Profile.as_view(),
         name="UpdateUserProfile"),

    # Login
    path("Login/", User_Login_Views.as_view(), name="UserLoginViews"),
    path("Verify_Login_OTP/", User_Verify_Email_OTP_Views.as_view(),
         name="VerifyLoginOTPViews"),
    # System Log
    path("System_log/", SystemAndDeviceLog_Create_Views.as_view(),
         name="SystemLogViews"),

    # Review
    path("Post_Review/", Post_Review_Views.as_view(), name="PostReviewsViews"),
    path("Get_Review_By_Rating/", Review_by_Rating_View.as_view(),
         name="GetReviewByRating"),

    # FAQ
    path("Create_FAQ/", Create_FAQ_views.as_view(), name="CreateFAQViews"),
    path("Update_FAQ/<int:pk>/", Update_FAQ_views.as_view(),
         name="UpdateReviewViews"),
    path("Delete_Soft_FAQ/<int:pk>/",
         DeleteSoft_FAQ_views.as_view(), name="DeleteSoftFAQ"),
    path("Get_Single_FAQ/<int:pk>/", Get_FAQ_views.as_view(), name="GetSingleFAQ"),
    path("List_All_FAQ/", List_FAQ_Views.as_view(), name="GetAllFAQ"),


    # Location
    path("Create_Location/", Create_Location_views.as_view(),
         name="CreateLocationViews"),
    path("List_Location/", List_Location_Views.as_view(), name="ListLocationViews"),


    # Proposal
    path("Create_Proposal/", Create_Proposal_views.as_view(), name="CreateProposal"),
    path("Cancel_proposal/<int:pk>/",
         cancel_proposal_view.as_view(), name="CancelProposalTrip"),
    path("List_offer_trip/", List_proposal_view.as_view(), name="ListALlProposal"),

    # Rider
    path("Create_Rider/", Create_Rider_views.as_view(), name="CreateRider"),
    path("List_ride/", List_rider_view.as_view(), name="ListRide"),
    path("Completed_ride/", List_Completed_rider_view.as_view(), name="CompletedRide"),
    path("Delete_ride/<int:pk>/", delete_ride_view.as_view(), name="DeleteRide"),
    path("Completed_ride/<int:pk>/",
         Complete_ride_view.as_view(), name="CompletedRide"),
]
