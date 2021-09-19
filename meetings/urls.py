from django.urls import path
from . import views


urlpatterns = [
    path("<str:meeting_id>", views.Meetings.as_view(),
         name="View Meeting Endpoint"),
]
