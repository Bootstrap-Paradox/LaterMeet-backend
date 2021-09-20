from pymongo import results
from pymongo.results import InsertOneResult, InsertManyResult
from BusinessInteraction import USER, MEETINGS
from pymongo.collection import Collection
from typing import Union


class Operations():

    __AUTH_REF = USER["auth"]
    __USER_REF = USER["user"]

    # Meetings Collection
    __MEETINGS_REF = MEETINGS["meetings"]

    def __init__(self):

        pass

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

    def delete(self, COLLECTION_REF: Collection = None, query: dict = None, all_instances=False):

        if all_instances:
            return COLLECTION_REF.delete_many(
                query
            )

        return COLLECTION_REF.delete_one(
            query
        )

    def __create_blueprint(self):
        pass
