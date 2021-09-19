from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class Meetings(APIView):

    def get(self, request, meeting_id=None, format=None):
        return Response(
            {},
            status=status.HTTP_200_OK,
        )
