from config import QUERIES_COLLECTION_NAME
from components import Utils


class Message:

    def __init__(self, sdk, hash=None):
        self.sdk = sdk
        self.collection = QUERIES_COLLECTION_NAME

        self.hash = hash
        self.id = None
        self.data = None
        self.query_type = None

        if hash:
            self.__find()

    def create(self, data, query_type):
        self.hash = Utils.generate_hash()
        self.data = data
        self.query_type = query_type

        self.save()

    def save(self):
        data_to_save = {
            "hash": self.hash,
            "id": self.id,
            "data": self.data,
            "query_type": self.query_type
        }

        self.sdk.db.update(
            # Collection name
            self.collection,

            # Find params
            {"hash": self.hash},

            # Data to be saved
            data_to_save,

            # Upsert = true
            True
        )

    def wrap_callback_data(self, data):
        return "{}:{}".format(self.hash, data)

    @staticmethod
    def unwrap_callback_data(encoded_data=""):
        """
        Get from encoded_data hash and data
        "EJRU89E3:2637" --> {"hash": "EJRU89E3", "data":2637}

        :param string encoded_data:
        :return:
        """
        delimiter_position = encoded_data.find(":")

        hash = None
        data = None

        if delimiter_position > -1:
            hash = encoded_data[:delimiter_position]
            data = encoded_data[delimiter_position + 1:]

        return {
            "hash": hash,
            "data": data
        }

    def __find(self):
        result = self.sdk.db.find_one(self.collection, {"hash": self.hash})

        self.__fill_model(result)

    def __fill_model(self, data):
        if data:
            self.hash = data.get("hash")
            self.id = data.get("id")
            self.data = data.get("data")
            self.query_type = data.get("query_type")
