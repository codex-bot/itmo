from components import Utils
from config import QUERIES_COLLECTION_NAME


class Query:

    def __init__(self, sdk):
        self.sdk = sdk
        # self.collection = QUERIES_COLLECTION_NAME

    # async def send_message(self, data):
    #     message = Message(self.sdk)
    #     pass

    def create(self, payload):


    def save_message(self, payload):
        message_hash = payload['want_response']
        message = Message(self.sdk, message_hash)
        message.id = payload['message_id']
        message.save()
        self.sdk.log("Message {} was saved as {}".format(message.id, message.hash))

    async def process(self, payload):
        self.sdk.log("Process query with payload {}".format(payload))

        # # Response with want_response param
        # if "want_response" in payload:
        #     hash = payload['want_response']
        #     id = payload['message_id']
        #
        #     message = Message(self.sdk, hash)
        #     message.id = id
        #     message.save()




        # todo get query hash and data from payload["data"]

        # todo find query by hash

        # todo process

        # todo update message

    def __get(self, payload):
        pass

    def __set(self, payload, data):
        pass


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

    def __find(self):
        result = self.sdk.db.find_one(self.collection, {"hash": self.hash})

        self.__fill_model(result)

    def __fill_model(self, data):
        if data:
            self.hash = data.get("hash")
            self.id = data.get("id")
            self.data = data.get("data")
            self.query_type = data.get("query_type")
