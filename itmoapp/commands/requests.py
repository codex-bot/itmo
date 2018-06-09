import random
import string
from time import time
import requests

from config import URL, USERS_COLLECTION_NAME
from .base import CommandBase



class CommandRequests(CommandBase):

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    async def __call__(self, payload):
        self.sdk.log("/requests handler fired with payload {}".format(payload))

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

        params = {
             'user_id': 1234
        }

        user_requests = requests.get(self.API_URL + 'requests', params=params, timeout=5).json()

        message = 'Ваша позиция в рейтинге:\n'

        print(user_requests)

        for request in user_requests['requests']:
            message += '{} / {} - {} \n'.format(request['position'], request['request']['slots']['budget'], request['request']['program'])


        await self.send(
            payload["chat"],
            message
        )
