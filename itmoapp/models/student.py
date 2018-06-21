from config import USERS_COLLECTION_NAME


class Student:

    def __init__(self, sdk, data=None, chat=None):
        self.sdk = sdk
        self.chat = None
        self.id = None
        self.name = None
        self.scores = None
        self.collection = USERS_COLLECTION_NAME

        if chat is not None:
            self.get(chat)
        elif data is not None:
            self.fill_model(data)

    def get(self, chat):
        """
        Get user data from db

        :param string chat:
        :return:
        """
        result = self.sdk.db.find_one(self.collection, {'chat': chat})

        self.fill_model(result)

    def save(self):
        data_to_save = {
            'chat': self.chat,
            'id': self.id,
            'name': self.name,
            'scores': self.scores
        }

        self.sdk.db.update(
            # Collection name
            self.collection,

            # Find params
            {'chat_id': self.chat},

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

    def fill_model(self, data):
        if data is None:
            return

        self.chat = data.get('chat')
        self.id = data.get('id')
        self.name = data.get('name')
        self.scores = data.get('scores')

    def get_positions(self):
        pass