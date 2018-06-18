class Base:

    def __init__(self, state_controller):
        self.sdk = state_controller.sdk
        self.controller = state_controller

    async def before(self, payload):
        pass

    async def process(self, payload):
        pass
