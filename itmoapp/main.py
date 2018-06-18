from sdk.codexbot_sdk import CodexBot
from config import *
from commands import *
from states import Controller as StateController


class Itmo:

    def __init__(self):
        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN, hawk_token=HAWK_TOKEN)

        self.sdk.log("Itmo module initialized")

        self.state_controller = StateController(self.sdk, STATES_COLLECTION_NAME)

        self.sdk.register_commands([
            ('itmo', 'start', CommandStart(self.sdk, self.state_controller))
        ])

        self.sdk.set_user_answer_handler(self.process_user_reply)

        self.sdk.start_server()

    async def process_user_reply(self, payload):
        self.sdk.log("User reply handler fired with payload {}".format(payload))

        await self.state_controller.process(payload)


if __name__ == "__main__":
    itmo = Itmo()
