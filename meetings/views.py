from utils.utility.utility import safe
from utils.operations.meetings import Meetings
from django.shortcuts import render
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
            meeting_document = Meetings(meeting_id=meeting_id).fetch_meeting()
            return Response(
                safe({**meeting_document}),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MeetingQuaters(APIView):

    def get(self, request, meeting_id=None):
        # TODO: Fetch Meeting from User id if Meeting Id not present

        try:
            pass

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):

        try:
            new_meeting: dict = Meetings().create_meeting(request.data)

            return Response(
                safe(new_meeting),
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, meeting_id=None, format=None):

        try:
            meeting_data = Meetings(
                meeting_id=meeting_id).update_meeting(request.data)
            return Response(
                {"msg": str(meeting_data)},
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
