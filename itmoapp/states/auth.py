from .base import Base


class StateAuth(Base):

    async def before(self, payload):
        message = "Введите номер заявления"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

    async def process(self, payload):
        self.sdk.log("State Start processor fired with payload {}".format(payload))

        text = payload['text']

        # TODO

        message = 'ну привет, студент №{}'.format(text)

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'start')
