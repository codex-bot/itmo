from itmoapp.states import *


class Controller:

    def __init__(self, sdk, collection):
        self.sdk = sdk
        self.collection = collection

        # Dict of available states
        self.states_list = {
            'auth': StateAuth,
            'greeting': StateGreeting,
            'start': StateStart
        }

    async def process(self, payload):
        """
        Trigger process command for current state

        :param dict payload:
        :return:
        """
        state_name = await self.get(payload)
        self.sdk.log("Process state {} for chat {}".format(state_name, payload['chat']))

        if state_name is None:
            return

        try:
            state_class = self.get_state_class(state_name)

            # Call process function for target state
            await state_class.process(payload)
        except Exception as e:
            self.sdk.log("Cannot process request with state {} because of {}".format(state_name, e))

    async def get(self, payload):
        """
        Get state from DB for target user&chat

        :param dict payload:
        :return string: state name
        """
        chat_state = self.sdk.db.find_one(self.collection, {'chat': payload['chat']})

        state_name = chat_state['name'] if chat_state else None

        return state_name

    async def set(self, payload, state=None):
        """
        Set state for target chat

        :param dict payload:
        :param string state:
        :return:
        """
        self.sdk.log("Set state {} for chat {}".format(state, payload['chat']))

        if not self.get_state_class(state):
            self.sdk.log("State with name {} is not exist".format(state))
            return

        chat_state = {
            'chat': payload['chat'],
            'name': state
        }

        self.sdk.db.update(
            self.collection,
            {'chat': chat_state['chat']},
            chat_state,
            True
        )

    async def goto(self, payload, state_name=None):
        """
        Change state and call its before function

        :param dict payload:
        :param string state_name:
        :return void:
        """
        self.sdk.log("GOTO state {}".format(state_name))

        # Update state
        await self.set(payload, state=state_name)

        if state_name is not None:
            # Call state's before function
            # TODO pass params from previews function
            await self.get_state_class(state_name).before(payload)

            await self.sdk.broker.api.wait_user_answer(
                payload['user'],
                payload['chat']
            )

    def get_state_class(self, name):
        """
        Get state class helper

        :param string name: state name
        :return:
        """
        return self.states_list[name](self) if name in self.states_list else None
