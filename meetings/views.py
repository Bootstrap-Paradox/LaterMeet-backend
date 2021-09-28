import traceback
from utils.operations.Errors import NotFound
from utils.utility.utility import authenticate_token, safe
from utils.operations.meetings import Meetings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from datetime import datetime

# Create your views here.


class MeetingsEndpoint(APIView):

    def get(self, request, meeting_id=None, format=None):
        try:
            timing = time.mktime(datetime.utcnow().timetuple()) * 1000
            meeting_document = Meetings(meeting_id=meeting_id).join_meeting()
            return Response(
                safe({**meeting_document}),
                status=status.HTTP_200_OK,
            )

        except NotFound as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MeetingQuaters(APIView):

    @authenticate_token
    def get(self, request, decoded_data, meeting_id=None):
        # TODO: Fetch Meeting from User id if Meeting Id not present

        try:
            meeting_doc: dict = Meetings(
                meeting_id=meeting_id, user_id=decoded_data["user_id"]).fetch_meeting()

            return Response(
                safe(meeting_doc),
                status=status.HTTP_200_OK
            )

        except NotFound as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @authenticate_token
    def post(self, request, decoded_data, format=None):

        try:
            new_meeting: dict = Meetings(
                user_id=decoded_data["user_id"]).create_meeting(request.data)

            return Response(
                safe(new_meeting),
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @authenticate_token
    def put(self, request, decoded_data, meeting_id=None, format=None):

        try:
            print(request.data)
            # Deleting the _id field
            del request.data["_id"]

            meeting_data = Meetings(
                user_id=decoded_data["user_id"],
                meeting_id=meeting_id).update_meeting(request.data)
            return Response(
                {"msg": str(meeting_data)},
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @authenticate_token
    def delete(self, request, decoded_data, meeting_id=None, format=None):

        try:
            Meetings(meeting_id=meeting_id,
                     user_id=decoded_data["user_id"]).delete_meeting()
            return Response(
                {"msg": "true"},
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
