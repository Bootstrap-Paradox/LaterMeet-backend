from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from utils.utility.utility import authenticate_token

# Views for User Account


class UserEndpoint(APIView):

    @authenticate_token
    def get(self, request, decoded_data, format=None):

        try:
            pass

        except Exception as e:
            return Response(
                {
                    "msg": "Work in progress"
                },
                status=status.HTTP_403_FORBIDDEN
            )

    @authenticate_token
    def post(self, request, decoded_data, format=None):
        pass

    @authenticate_token
    def put(self, request, decoded_data, format=None):
        pass

    @authenticate_token
    def delete(self, request, decoded_data, format=None):
        pass
