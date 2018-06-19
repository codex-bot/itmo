class Base:

    def __init__(self, state_controller):
        self.sdk = state_controller.sdk
        self.controller = state_controller

        self.response_phrases = {}

    async def before(self, payload, data):
        pass

    async def process(self, payload, data):
        pass

    # async def send_message(self, payload, message):
    #     await self.sdk.send_text_to_chat(
    #         payload["chat"],
    #         message
    #     )

    # async def parse_response(self, text):
    #     for tag in self.response_phrases:
