from BusinessInteraction import USER

from datetime import datetime, timedelta
from utils.authentication.authentication import Authentication
from utils.authentication.Errors import *
import bcrypt as bc


def hashPassword(password):
    return bc.hashpw(bytes(password, 'utf-8'), bc.gensalt())


def checkPassword(password, hashed_password):
    return bc.checkpw(bytes(password, 'utf-8'), hashed_password)

# User Authentication


class User_Authentication(Authentication):

    def __init__(self):
        self.AUTH_REF = USER["auth"]
        self.USER_REF = USER["user"]

    def authentication(self):
        pass

    def _check_existing_user_with_email(self, email):
        if self.AUTH_REF.find_one(
            {"email": email}
        ):
            # Returns True if the User Exists in the database
            return True

        # Returns False when No user with provided email is found
        return False

    def signup(self, user_data):
        # Inserting the Password in the Hashed format to the Server

        try:
            if (not (user_data["email"] == "" and user_data["password"] == "")):
                if self._check_existing_user_with_email(user_data["email"]):
                    raise UserAlreadyExistError(user_data["email"])

                # Generating User Details and Inserting in the Server
                inserted_user_doc = self.USER_REF.insert_one(self.generate_user_template(
                    user_data))

                # Inserting Authentication Details on the Server
                inserted_auth_doc = self.AUTH_REF.insert_one({
                    "email": user_data["email"],
                    "password": hashPassword(user_data["password"]),
                    "user_id": inserted_user_doc.inserted_id,
                    "last_login": datetime.utcnow(),
                    "created_on": datetime.utcnow()
                })

                return {"access_token": self.generate_access_token({"user_id": str(inserted_user_doc.inserted_id)})}

            else:
                # Raising Error when the email of password are empty
                raise AuthenticationError("Fields Cannot Be Empty")

        except Exception as e:
            raise e

        # Must Store the authentication id in the user Database

    def login(self, user_credentials):
        try:
            if user_credentials["email"] == "" and user_credentials["password"] == "":
                raise AuthenticationError("Fields Cannot be Empty")

            auth = self.AUTH_REF.find_one_and_update(
                {"email": user_credentials["email"]},
                {"$set": {
                    "last_login": datetime.utcnow()
                }}
            )

            auth = self.AUTH_REF.find_one({"email": user_credentials["email"]})
            if not auth:
                raise UserNotFound(email=user_credentials["email"])

            if not checkPassword(user_credentials["password"], auth["password"]):
                raise AuthenticationError("Incorrect Password")

            return {"access_token": self.generate_access_token({"user_id": str(auth["user_id"])})}
        except Exception as e:
            raise e

    def generate_user_template(
        self,
        user_data: dict = None,
    ):
        if not isinstance(user_data, dict):
            raise AttributeError("Dictonary Required to Read User Data")

        return {
            "firstName": user_data.get("firstName", ""),
            "lastName": user_data.get("lastName", ""),
            "email": user_data.get("email", ""),
            "meeting_ids": [],
        }
