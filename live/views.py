from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import time

# Create your views here.


class Live(APIView):

    def get(self, request, meeting_id, format=None):

        return Response({
            "meeting_start_time": time.mktime(datetime.utcnow().timetuple()) * 1000,
            "meeting_name": "Dale Webinar",
            "meeting_url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        }, status=status.HTTP_200_OK)
