from sdk.codexbot_sdk import CodexBot
from config import *
from commands import *
from states import *
from queries import *
from components import Methods, Webserver
# from models.student import USERS_COLLECTION_NAME
import re


class Itmo:

    def __init__(self):
        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN, hawk_token=HAWK_TOKEN)
        self.sdk.log("Itmo module initialized")

        # Set up states
        self.state_controller = State(self.sdk)
        self.state_controller.states_list = {
            'ask_auth_correctness': StateAskAuthCorrectness,
            'ask_scores': StateAskScores,
            'auth': StateAuth,
            'calc': StateCalc,
            'greeting': StateGreeting,
            'menu': StateMenu,
            'ratings': StateRatings,
            'settings': StateSettings,
            'start': StateStart
        }

        # Set up queries
        self.query_controller = Query(self.sdk)

        # Set up commands
        self.sdk.register_commands([
            ('itmo_start', 'start', CommandStart(self.sdk, self.state_controller)),
            ('itmo_help', 'help', CommandHelp(self.sdk, self.state_controller))
        ])

        # Define text answer handler
        self.sdk.set_user_answer_handler(self.process_user_answer)

        # Define query handler
        self.sdk.set_callback_query_handler(self.process_callback_query)

        # Restore jobs in scheduler
        self.sdk.scheduler.restore(Methods(self.sdk).loggy)

        # Set up and run webserver
        self.webserver = Webserver(self.sdk)

    async def process_user_answer(self, payload):
        self.sdk.log("User reply handler fired with payload {}".format(payload))

        # We have no command in user's message
        command_in_text = None

        try:
            # Try to find command in text message
            command_in_text = re.match(r"/([\w]+)", payload.get('text'))[0]

            # Remove first slash
            command_in_text = command_in_text[1:]
        except Exception as e:
            pass

        # Force run command if it was passed
        if payload.get('command') or command_in_text:
            # Get a command without slash from payload
            payload['command'] = payload.get('command', command_in_text)

            # Try to process command
            try:
                return await self.sdk.broker.api.service_callback(payload)

            # Well we don't care if something went wrong
            except Exception as e:
                # Do not return anything and process message as normal way
                pass

        # Process message as user's reply
        await self.state_controller.process(payload)

    async def process_callback_query(self, payload):
        self.sdk.log("Callback query handler fired with payload {}".format(payload))

        # Save message id if identifier was passed in want_response field from core
        if "want_response" in payload:
            return self.query_controller.save_message_id(payload)

        # Process query
        await self.query_controller.process(payload)


if __name__ == "__main__":
    itmo = Itmo()
