from utils.utility.mail import MailAuthenticateUser

from utils.operations.Errors import NotAllowed, Restricted
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


class Signup(APIView):

    def post(self, request, format=None):

        try:
            code = User().create_code(request.data)
            MailAuthenticateUser().mail(
                subject="Authentication Code",
                html_template_data=(
                    "authentication/code_authentication.html", {"code": code}),
                from_email="pyrabrain@gmail.com",
                to=[request.data["email"]]
            )
            return Response({"message": "Code Successful Sent"}, status=status.HTTP_201_CREATED)

        except UserAlreadyExistError:
            traceback.print_exc()
            return Response({"message": "User Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()

            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            if code_authenticated := User().auth(request.data["code"]):
                return Response(
                    {**code_authenticated},
                    status=status.HTTP_200_OK
                )
            raise NotAllowed("Code Incorrect")

        except NotAllowed as e:
            traceback.print_exc()
            return (Response(
                {"error": str(e)},
                status=status.HTTP_204_NO_CONTENT,
            ))

        except Restricted as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
