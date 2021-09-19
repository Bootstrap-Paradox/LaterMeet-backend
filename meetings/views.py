from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from datetime import datetime

# Create your views here.


class Meetings(APIView):

    def get(self, request, meeting_id=None, format=None):
        timing = time.mktime(datetime.utcnow().timetuple()) * 1000
        return Response(
            {},
            status=status.HTTP_200_OK,
        )
