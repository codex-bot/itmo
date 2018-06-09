import random
import string
from time import time

from config import URL, USERS_COLLECTION_NAME
from .base import CommandBase

class CommandLogin(CommandBase):

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    async def __call__(self, payload):
        self.sdk.log("/login handler fired with payload {}".format(payload))

        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': payload['chat']})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': payload['chat'],
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(USERS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        student_id = payload["params"]
        message = 'Неверный логин'

        if student_id != '':
            message = 'Добро пожаловать, Андрей'

        await self.send(
            payload["chat"],
            message
        )
