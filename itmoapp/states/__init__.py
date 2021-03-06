from .ask_auth_correctness import StateAskAuthCorrectness
from .ask_scores import StateAskScores
from .auth import StateAuth
from .calc import StateCalc
from .greeting import StateGreeting
from .menu import StateMenu
from .ratings import StateRatings
from .settings import StateSettings
from .start import StateStart
from components import Utils
from config import STATES_COLLECTION_NAME


class State:
    """
    Class for working with states
    """

    def __init__(self, sdk):
        self.sdk = sdk
        self.collection = STATES_COLLECTION_NAME

        # Dict of available states
        self.states_list = {}

    async def goto(self, payload, state_name=None, data=None):
        """
        Change state and call its before function

        Example:
        > return await self.controller.goto(payload, 'auth', {'login': 'user273'})

        :param dict payload:
        :param string state_name:
        :param dict data:
        :return void:
        """
        self.sdk.log("GOTO state {}".format(state_name))

        # Update state
        self.__set(payload, state=state_name, data=data)

        if state_name is not None:
            # Call state's before function
            await self.get_state_class(state_name).before(payload, data)

            # Call wait user answer
            await self.sdk.broker.api.wait_user_answer(
                payload['user'],
                payload['chat'],
                bot=payload.get('bot', None)
            )

    async def process(self, payload, data=None):
        """
        Trigger process() command for current state

        :param dict payload:
        :param data:
        :return:
        """
        # Get current state from DB
        state = self.__get(payload)
        self.sdk.log("Process state {} for chat {}".format(state['name'] if state else None, payload['chat']))

        # If state name is missing the return null
        if not state or 'name' not in state:
            return

        # Find state class in map
        state_class = self.get_state_class(state['name'])

        # Call process function for target state
        await state_class.process(payload, data if data is not None else state['data'])

    async def reenter(self, payload):
        """
        Reenter to current state

        :param payload:
        :return:
        """
        # Get current state from DB
        current_state = self.__get(payload)

        # Do nothing if current state in none
        if current_state is None:
            return

        # Enter to current state again
        await self.goto(payload, current_state['name'], current_state['data'])

    def is_state_exist(self, name):
        """
        Check for a state existing

        :param string name:
        :return boolean:
        """
        # Check for a state with target name existing in a states_list dict
        return name in self.states_list

    def get_state_class(self, name):
        """
        Get state class helper if it is exists

        :param string name: state name
        :return:
        """
        # If state is not exist then throw an exception
        if not self.is_state_exist(name):
            raise Exception('Can not find class for state {}'.format(name))

        # Otherwise return state class
        return self.states_list[name](self)

    def __get(self, payload):
        """
        Get state from DB for target chat

        :param dict payload:
        :return dict: state from db: _id, chat, name, data, class
        """
        # Get current state from db
        current_state = self.sdk.db.find_one(
            Utils.create_collection_name(self.collection, payload),
            {'chat': payload['chat']}
        )

        # Return None if state is missing
        if not current_state:
            return None

        # Fill class param in dictionary
        current_state['class'] = self.get_state_class(current_state['name'])

        # Return current state data
        return current_state

    def __set(self, payload, state=None, data=None):
        """
        Set state for target chat

        Example:
        > await self.set(payload, state='start', data=None)

        :param dict payload:
        :param string state:
        :param dict data:
        :return:
        """
        self.sdk.log("Set state {} for chat {}".format(state, payload['chat']))

        # If unexisted state was passed then throw an exception
        if not self.is_state_exist(state):
            raise Exception("State with name {} is not exist".format(state))

        # Prepare state data to be saved
        chat_state = {
            # Target chat
            'chat': payload['chat'],

            # State name
            'name': state,

            # Additional data for state
            'data': data
        }

        # Update state for target chat in db
        self.sdk.db.update(
            # Collection name
            Utils.create_collection_name(self.collection, payload),

            # Find params
            {'chat': chat_state['chat']},

            # Data to be saved
            chat_state,

            # Upsert = true
            True
        )

