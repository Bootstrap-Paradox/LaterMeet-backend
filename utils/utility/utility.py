import json
from bson.objectid import ObjectId
import datetime
import uuid
import jwt
from rest_framework.response import Response
from rest_framework import status
import os
from pymongo.cursor import Cursor


def safe(data: dict) -> dict:
    return json.loads(JSONEncoder().encode(data))


class JSONEncoder(json.JSONEncoder):

    def default(self, o: any) -> any:
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        if isinstance(o, uuid.UUID):
            return str(o)

        if isinstance(o, Cursor):
            return list(o)

        return json.JSONEncoder.default(self, o)


def authenticate_token(function):
    def wrapper(*args, **kwargs):
        self, request, *data = args
        access_token_header: str = request.headers.get("authorization", None)
        try:
            if access_token_header:

                access_token = access_token_header.split(" ")[1]

                decoded_data = jwt.decode(
                    access_token, key=os.environ["JWT_SECRET_KEY"], algorithms=["HS256"])

                return function(self, request, decoded_data, *data, **kwargs)
            else:
                print("login to interact")
                return Response({"notify": [{"status": "danger", "message": "Login to Interact"}]}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            print("you are not allowed")
            return Response({"notify": [{"status": "danger", "message": "Unauthorized"}]}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
