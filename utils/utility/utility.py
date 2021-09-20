import json
from bson.objectid import ObjectId
import datetime
import uuid


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

        return json.JSONEncoder.default(self, o)
