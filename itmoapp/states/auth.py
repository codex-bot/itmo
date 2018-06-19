from .base import Base


class StateAuth(Base):

    async def before(self, payload, data):
        message = "Введите номер заявления"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

    async def process(self, payload, data):
        self.sdk.log("State Start processor fired with payload {}".format(payload))

        text = payload['text']

        # todo parse user id

        # todo if parsing was failed
            # todo show error message
            # todo goto auth

        # todo api request user

        # todo if user in response is null
            # todo show error message
            # todo goto auth

        # todo show message "are you alexey?"

        #
        #
        # message = 'ну привет, студент №{}'.format(text)
        #
        # await self.sdk.send_text_to_chat(
        #     payload["chat"],
        #     message
        # )

        data = {
            'id': 123456789,
            'name': 'Андрей Федотов',

        }

        return await self.controller.goto(payload, 'ask_auth_correctness', data)
