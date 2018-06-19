from itmoapp.config import USERS_COLLECTION_NAME


class Student:

    def __init__(self, sdk, data=None, chat=None):
        self.sdk = sdk
        self.chat_id = ''
        self.id = 0
        self.name = ''
        self.scores = []

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
        result = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': chat})
        self.sdk.log("[DB] get result: {}".format(result))

    async def save(self):
        pass

    async def fill_model(self, data):
        self.chat_id = data.get('chat_id', 0)
        self.id = data.get('id', 0)
        self.name = data.get('name', '')
        self.scores = data.get('test_scores', [])

    def get_positions(self):
        """

        :return:
        """
        pass