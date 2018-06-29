from queries import Query


class Base:

    def __init__(self, state_controller):
        self.sdk = state_controller.sdk
        self.controller = state_controller

        # todo remove this var
        self.queries = Query(self.sdk)

        self.response_phrases = {}

    async def before(self, payload, data):
        """
        State's before called when user enters this state.
        Controller's goto() and reenter() fire this function.

        :param payload:
        :param data:
        :return:
        """
        pass

    async def process(self, payload, data):
        """
        Process function called on a new user's message while he is in a state.
        Anyone can fire this function for current state by calling Controller's
        process() function.

        :param payload:
        :param data:
        :return:
        """
        pass

# todo add a function to parse user's response (choose right in self.response_phrases)
# todo add regex support
