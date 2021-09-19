from django.urls import path
from . import views

urlpatterns = [
    path("<str:meeting_id>", views.Live.as_view(), name="Meeting Endpoint")
]
