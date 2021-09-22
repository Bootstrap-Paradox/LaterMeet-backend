from utils.operations.Errors import Error, NotAllowed, Restricted
from bson.objectid import ObjectId
from pymongo import results
from pymongo.results import DeleteResult, InsertOneResult, InsertManyResult
from BusinessInteraction import USER, MEETINGS
from pymongo.collection import Collection
from typing import Union
from functools import wraps


class Operations():

    __AUTH_REF = USER["auth"]
    __USER_REF = USER["user"]

    # Meetings Collection
    __MEETINGS_REF = MEETINGS["meetings"]

    def __init__(self, user_id=None, meeting_id=None):
        self.user_id = user_id and ObjectId(user_id)
        self.meeting_id = meeting_id and ObjectId(meeting_id)

    # Properties

    @property
    def AUTH_REF(self):
        return self.__AUTH_REF

    @property
    def USER_REF(self):
        return self.__USER_REF

    @property
    def MEETINGS_REF(self):
        return self.__MEETINGS_REF

    # Decorators

    @staticmethod
    def verify_request(func):

        @wraps(func)
        def wrapper(self: Operations, *args, **kwargs):
            if not (user_info := self.find(
                self.USER_REF,
                {
                    "_id": self.user_id,
                    "meeting_ids": {
                        "$in": [self.meeting_id]
                    }
                },
            )):
                raise Restricted("Request Not Associated with Meeting")
            return func(self, user_info, *args, **kwargs)

        return wrapper

    @staticmethod
    def verify_user(func):
        @wraps(func)
        def wrapper(self: Operations, *args, **kwargs):
            if not (user_info := self.find(
                self.USER_REF,
                {
                    "_id": self.user_id,
                }
            )):
                raise NotAllowed("User Not Found")

            return func(self, user_info, *args, **kwargs)

        return wrapper

    # Mongo Funtionlity

    def insert(self, COLLECTION_REF: Collection, document, ordered=True, bypass_document_validation=False, session=None) -> Union[InsertManyResult, InsertOneResult]:
        if isinstance(document, list):
            return COLLECTION_REF.insert_many(document, ordered=ordered, bypass_document_validation=bypass_document_validation, session=session)
        return COLLECTION_REF.insert_one(document, bypass_document_validation=bypass_document_validation, session=session)

    def find(self, COLLECTION_REF: Collection = None, query: dict = None, options: dict = None, all_instance=False) -> list:

        if isinstance(options, type(None)):

            if all_instance:
                return COLLECTION_REF.find(
                    query,

                )

            return COLLECTION_REF.find_one(
                query,
            )

        if all_instance:
            return COLLECTION_REF.find(
                query,
                options
            )

        return COLLECTION_REF.find_one(
            query,
            options
        )

    def find_and_modify(self, COLLECTION_REF: Collection = None, query: dict = None, modify: dict = None):

        return COLLECTION_REF.find_and_modify(
            query,
            modify
        )

    def update(
        self,
        COLLECTION_REF: Collection = None,
        query: dict = None,
        update=None,
        upsert=False,
        bypass_document_validation=False,
        collation=None,
        array_filters=None,
        hint=None,
        session=None,
        all_instances=False,
    ):
        """Update One or More Documents that match the query.

        """

        if all_instances:

            return COLLECTION_REF.update_many(
                query,
                update,
                upsert=upsert,
                bypass_document_validation=bypass_document_validation,
                collation=collation,
                array_filters=array_filters,
                hint=hint,
                session=session
            )

        return COLLECTION_REF.update_one(
            query,
            update,
            upsert=upsert,
            bypass_document_validation=bypass_document_validation,
            collation=collation,
            array_filters=array_filters,
            hint=hint,
            session=session
        )

    def delete(self, COLLECTION_REF: Collection = None, query: dict = None, all_instances=False) -> DeleteResult:

        if all_instances:
            return COLLECTION_REF.delete_many(
                query
            )

        return COLLECTION_REF.delete_one(
            query
        )

    def __create_blueprint(self):
        pass
