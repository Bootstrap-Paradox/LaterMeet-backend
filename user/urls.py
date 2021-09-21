from django.urls import path
from . import views

urlpatterns = [
    path("login", views.Login.as_view(), name="User Login"),
    path("signup", views.Signup.as_view(), name="User Signup"),
]
