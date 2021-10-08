

from utils.operations import Operations
from utils.operations.Errors import NotAllowed, NotFound


class User(Operations):

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def create_personal_information(self):
        # Create personal information on Create Account
        """
        Deprecated
        """
        pass

    def fetch_personal_information(self):
        if not (user_info := self.find(
            self.USER_REF,
            {
                "_id": self.user_id,
            }
        )):
            raise NotFound("Could Not find user")

        return user_info

    def update_personal_information(self, update_data=None):

        # Checks for update data

        if not update_data:
            # Raise when empty data passed -> Rare case
            NotAllowed("Meeting Data cannot be empty")

        if "meeting_ids" in update_data:
            del update_data["meeting_ids"]

        if self.update(
            self.USER_REF,
            {
                "_id": self.user_id,
            },
            {
                "$set": update_data
            }
        ).modified_count == 0:
            raise NotFound("User Information could Not be Updated")

        return True

    def delete_account(self):

        # Temprary Solution
        # -> Future Editions Manages Meetings related with the account

        if self.delete(
            self.USER_REF,
            {
                "_id": self.user_id,
            }
        ).deleted_count == 0:
            raise NotFound("User Could Not be deleted")

        return True
