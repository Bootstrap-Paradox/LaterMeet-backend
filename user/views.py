from django.shortcuts import render

from utils.authentication.Errors import NotAllowed
from utils.authentication.Errors import *
from .models import User
from rest_framework.views import APIView
# from utils.mail_utility import MailAuthenticateUser
from rest_framework import status
from rest_framework.response import Response

import traceback

from utils.authentication.user_authentication import User_Authentication

# Create your views here.

auth = User_Authentication()


class Login(APIView):

    def post(self, request, format=None):
        data = {}
        try:
            token = auth.login(request.data)

            return Response(token, status=status.HTTP_200_OK)

        except UserNotFound as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except AuthenticationError as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
