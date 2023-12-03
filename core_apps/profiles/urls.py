from django.urls import path
from .views import *

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("my-profile/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("my-profile/update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("my-profile/followers/", FollowerListView.as_view(), name="followers"),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]
