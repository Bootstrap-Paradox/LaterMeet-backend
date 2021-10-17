import jwt
from os import environ
from datetime import datetime, timedelta


def payload_check(function):
    def wrapper(*args, **kwargs):
        self, payload, *data = args
        if not isinstance(payload, dict):
            raise TypeError(
                f"Argument Accepts property of dict, but {type(payload)} was passed")

        return function(self, payload, *data, **kwargs)
    return wrapper


class Authentication:

    # On Login Storing the Refresh token in the database
    # sending out the access token to the user
    # on Invalid Access token request the auth server to generate a new Access token with the Refresh token in the database

    def __init__(self):
        pass

    @payload_check
    def generate_access_token(self, payload: dict = None) -> str:
        payload["exp"] = datetime.utcnow() + timedelta(days=1)
        payload["iat"] = datetime.utcnow()
        token = jwt.encode(payload, key=environ["JWT_SECRET_KEY_LATERMEET"])
        return token

    @payload_check
    def generate_refresh_token(self, payload):
        token = jwt.encode(payload, key="SecretNotYetDecided")
        return {"access_token": self.generate_access_token(payload), "refresh_token": token}

    def __store_refresh_token(self):
        # Stores the data to the database
        pass

    def authenticate_access_token(self, access_token: str) -> dict:
        return jwt.decode(access_token, key=environ["JWT_SECRET_KEY_LATERMEET"])

    def authenticate_refresh_token(self):
        pass
