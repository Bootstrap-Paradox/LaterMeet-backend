from utils.operations.Errors import NotFound
from . import Operations
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import time


class Meetings(Operations):

    def __init__(self, meeting_id, *args, **kwargs):
        super(Meetings, self).__init__(*args, **kwargs)
        self.meeting_id = meeting_id and ObjectId(meeting_id)

    def fetch_meeting(self):
        # TODO: Time Check with Request Timezone
        if not (meeting_doc := self.find(
            self.MEETINGS_REF,
            {
                "_id": self.meeting_id
            }
        )):
            NotFound(f"Meeting with {str(self.meeting_id)} Not Found")

        return meeting_doc

    def create_meeting(self, meeting_data: dict):
        pass

    def __create_blueprint(self, meeting_data: dict = None) -> dict:
        return {
            "meeting_name": meeting_data.get("meeting_name", ""),
            "meeting_description": meeting_data.get("meeting_description", ""),
            "meeting_url": meeting_data.get("meeting_url", None),
            "meeting_recursive": meeting_data.get("meeting_recursive", False),
            "meeting_hosts": [],
            "meeting_speakers": []
        }
