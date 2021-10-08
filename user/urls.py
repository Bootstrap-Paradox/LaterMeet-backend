from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserEndpoint.as_view(), name="User Endpoint"),
    path("<str:user_id>", views.UserEndpoint.as_view(),
         name="User Endpoint with userId"),

]
