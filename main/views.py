from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.


class Main(APIView):

    def get(self, request, format=None):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        return Response(
            {"msg": "data from the Server"},
            status=status.HTTP_200_OK
        )
