from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from utils.authentication import User
from utils.utility.utility import safe
from utils.utility.utility import authenticate_token
import traceback

# Views for User Account


class UserEndpoint(APIView):

    @authenticate_token
    def get(self, request, decoded_data, user_id=None, format=None):

        try:
            user_data = User(
                user_id=decoded_data["user_id"]).fetch_personal_information()

            return Response(
                safe(user_data),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "msg": str(e)
                },
                status=status.HTTP_403_FORBIDDEN
            )

    @authenticate_token
    def put(self, request, decoded_data, format=None):
        try:
            if not User(user_id=decoded_data["user_id"]).update_personal_information(request.data):
                pass

            return Response(
                {},
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {
                    "msg": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @authenticate_token
    def delete(self, request, decoded_data, user_id=None, format=None):

        try:
            # if decoded_data["user_id"] != user_id:
            #     raise NotAllowed("User Ids don't match")

            if not User(user_id=decoded_data["user_id"]).delete_account():
                pass

            return Response(
                {},
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
