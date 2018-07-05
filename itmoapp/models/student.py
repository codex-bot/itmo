from components import Utils
from config import STUDENTS_COLLECTION_NAME


class Student:

    def __init__(self, sdk, payload, data=None, chat=None):
        self.sdk = sdk
        self.chat = None
        self.id = None
        self.name = None
        self.scores = None
        self.programs = None
        self.collection = Utils.create_collection_name(STUDENTS_COLLECTION_NAME, payload)

        if chat is not None:
            self.__get(chat)
        elif data is not None:
            self.__fill_model(data)

    def save(self):
        data_to_save = {
            'chat': self.chat,
            'id': self.id,
            'name': self.name,
            'scores': self.scores,
            'programs': self.programs
        }

        self.sdk.db.update(
            # Collection name
            self.collection,

            # Find params
            {'chat': self.chat},

            # Data to be saved
            data_to_save,

            # Upsert = true
            True
        )

    def remove(self):
        self.sdk.db.remove(
            # Collection name
            self.collection,

            # Find params
            {'chat': self.chat}
        )

    def __get(self, chat):
        """
        Get user data from db

        :param string chat: chat_hash from payload
        :return:
        """
        result = self.sdk.db.find_one(self.collection, {'chat': chat})

        self.__fill_model(result)

    def __fill_model(self, data):
        if data is None:
            return

        self.chat = data.get('chat')
        self.id = data.get('id')
        self.name = data.get('name')
        self.scores = data.get('scores')
        self.programs = data.get('programs')
