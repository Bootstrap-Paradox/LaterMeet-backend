from utils.operations.Errors import NotAllowed, NotFound
from . import Operations
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import time
from pymongo.cursor import Cursor


class Meetings(Operations):

    def __init__(self, *args, **kwargs):
        super(Meetings, self).__init__(*args, **kwargs)

    @staticmethod
    def find_cloest(timings: list = None):
        # TODO: type Check for list
        if timings:
            current_time = datetime.utcnow()
            cloest_diff = abs(timings[0] - current_time)
            cloest_index = 0
            index = 0
            for timing in timings:
                if (diff := abs(timing - current_time)) < cloest_diff:
                    cloest_diff = diff
                    cloest_index = index
                index += 1

            return time.mktime(timings[cloest_index].timetuple()) * 1000

        return None

    def join_meeting(self):
        # TODO: Time Check with Request Timezone
        if not (meeting_doc := self.MEETINGS_REF.find_one_and_update(
            {
                "_id": self.meeting_id,
            },
            {
                "$inc": {
                    "meeting_views": 1,
                }
            }
        )):
            raise NotFound(f"Meeting with {str(self.meeting_id)} Not Found")

        meeting_doc["meeting_start_time"] = self.find_cloest(
            meeting_doc["meeting_timings"]) or time.mktime(datetime.utcnow().timetuple()) * 1000

        del meeting_doc["meeting_timings"]

        return meeting_doc

    @Operations.verify_user
    def create_meeting(self, user_info, meeting_data: dict) -> dict:
        # Create Meeting
        inserted_meeting = self.insert(
            self.MEETINGS_REF, self.__create_blueprint(meeting_data, host_name=f"{user_info['firstName']} {user_info['lastName']}"))

        self.update(
            self.USER_REF,
            {
                "_id": self.user_id,
            },
            {
                "$addToSet": {
                    "meeting_ids": inserted_meeting.inserted_id,
                }
            }
        )

        # TODO: Add inserted_id to user database
        return {"meeting_id": inserted_meeting.inserted_id}

    # @Operations.verify_request
    def fetch_meeting(self) -> dict:
        response_data = {}

        def fetch_name(meeting_doc):
            if meeting_doc.count() == 0:
                raise NotFound("Meetings Not Found")
            return [
                host["name"] for host in meeting_doc["meeting_hosts"] if str(host["_id"]) == str(self.user_id)][0] if not isinstance(meeting_doc, Cursor) else [
                host["name"] for host in meeting_doc[0]["meeting_hosts"] if str(host["_id"]) == str(self.user_id)][0]

        if (self.meeting_id):

            if not (meeting_doc := self.find(
                self.MEETINGS_REF,
                {
                    "_id": self.meeting_id,
                    "meeting_hosts": {
                        "$elemMatch": {
                            "_id": self.user_id
                        }
                    }
                }
            )):
                raise NotFound("Meeting Does Not Exist")

            response_data["meeting_data"] = meeting_doc

            response_data["request_name"] = fetch_name(meeting_doc)

        else:
            if not (meeting_doc := self.find(
                self.MEETINGS_REF,
                {
                    "meeting_hosts": {
                        "$elemMatch": {
                            "_id": self.user_id
                        }
                    }
                },
                all_instance=True
            )):

                raise NotFound("Meetings not Found")
            response_data["meetings"] = meeting_doc
            response_data["request_name"] = fetch_name(meeting_doc)

        return {**response_data}

    @Operations.verify_request
    def update_meeting(self, user_info, updated_meeting_data: dict) -> bool:
        # TODO: Check User Authenticity
        if (updated_data := self.update(
            self.MEETINGS_REF,
            {
                "_id": self.meeting_id,
            },
            {
                "$set":
                updated_meeting_data
            }
        )).modified_count == 0:
            raise NotFound(f"Meeting with {self.meeting_id} Not Found")

        return True

    @Operations.verify_request
    def delete_meeting(self, user_info: dict) -> bool:
        # TODO: Authenticate User Before Operation

        if not self.meeting_id:
            raise NotAllowed("Operation Requires Id")
        if self.delete(
            self.MEETINGS_REF,
            {
                "_id": self.meeting_id
            }
        ).deleted_count == 0:
            raise NotFound("Document with Id Not Found")

        return True

    def __create_blueprint(self, meeting_data: dict = None, host_name="") -> dict:
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
            "meeting_hosts": [{"_id": self.user_id, "name": host_name, "owner": True}],
            "meeting_speakers": [],
            "meeting_timings": [],
            "meeting_views": 0,
        }
