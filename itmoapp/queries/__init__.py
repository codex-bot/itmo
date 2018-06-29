from queries.types import *
from .base import Base
from .message import Message


class Query:

    def __init__(self, sdk):
        self.sdk = sdk

        # todo init it empty
        self.types_list = {
            QueryTypePagination.name(): QueryTypePagination
        }

    async def create(self, payload, data, query_type):
        """
        Create a new query message by target type

        :param payload:
        :param data:
        :param query_type:
        :return:
        """
        type_class = self.__get_type(query_type)
        await type_class.create(payload, data)

    def save_message_id(self, payload):
        """
        Save message id passed from core

        :param payload:
        :return:
        """
        message_hash = payload["want_response"]
        message = Message(self.sdk, message_hash)
        message.id = payload["message_id"]
        message.save()
        self.sdk.log("Message {} was saved as {}".format(message.id, message.hash))

    async def process(self, payload):
        self.sdk.log("Process query with payload {}".format(payload))

        # Unwrap hash and data
        # "7IEV0WJC:4" --> {"hash": "7IEV0WJC", "data": "4"}
        callback_data = Message.unwrap_callback_data(payload["data"])

        # Find message by hash in callback data
        message = Message(self.sdk, callback_data["hash"])

        type_class = self.__get_type(message.query_type)
        type_class.message = message

        await type_class.process(payload, callback_data["data"])

    def __get_type(self, query_type):
        """
        Get Type class by name

        :param query_type:
        :return:
        """
        if query_type not in self.types_list:
            raise Exception("Type with name {} does not exist".format(query_type))

        return self.types_list[query_type](self.sdk)
