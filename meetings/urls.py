from django.urls import path
from . import views


urlpatterns = [
    path("<str:meeting_id>", views.MeetingsEndpoint.as_view(),
         name="View Meeting Endpoint"),
    path("", views.MeetingQuaters.as_view(),
         name="Meeting Quaters -> only Host Access"),
]
