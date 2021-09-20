from utils.operations.Errors import NotFound
from . import Operations
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import time


class Meetings(Operations):

    def __init__(self, meeting_id=None, *args, **kwargs):
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

    def create_meeting(self, meeting_data: dict) -> dict:
        # Create Meeting
        inserted_meeting = self.insert(
            self.MEETINGS_REF, self.__create_blueprint(meeting_data))

        # TODO: Add inserted_id to user database
        return {"meeting_id": inserted_meeting.inserted_id}

    def update_meeting(self, updated_meeting_data: dict) -> bool:
        # TODO: Check User Authenticity
        if (updated_data := self.update(
            self.MEETINGS_REF,
            {
                "_id": self.meeting_id,
            },
            {
                "$set": updated_meeting_data
            }
        )) == 0:
            raise NotFound(f"Meeting with {self.meeting_id} Not Found")

        return True

    def __create_blueprint(self, meeting_data: dict = None) -> dict:
        """
        meeting_timmings: [
            {
                start_time: datetime(),
            }
        ]

        "meeting_meta_data": {
            "view_once": meeting_data.get("meeting_view_once", False),
            "allowed_viewers": meeting_data.get("meeting_allowed_viewers", []),
        }"""
        # "meeting_recursive": meeting_data.get("meeting_recursive", False),
        return {
            "meeting_name": meeting_data.get("meeting_name", ""),
            "meeting_description": meeting_data.get("meeting_description", ""),
            "meeting_url": meeting_data.get("meeting_url", None),
            "meeting_hosts": [],
            "meeting_speakers": [],
            "meeting_timings": [],
        }
