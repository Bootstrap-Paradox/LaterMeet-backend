from pymongo import MongoClient
import os

MONGO_USERNAME = os.environ.get("MONGO_USERNAME_LATERMEET")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD_LATERMEET")

connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.jzwjm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

CLIENT = MongoClient(connection_string, connect=False)

USER = CLIENT["User"]

MEETINGS = CLIENT["Meetings"]
