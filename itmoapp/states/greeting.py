from .base import Base


class StateGreeting(Base):

    def __init__(self, state_controller):
        super().__init__(state_controller)

        self.response_phrases = {
            'yes': [
                'Да, у меня уже есть номер',
                'Да'
            ],

            'no': [
                'Нет, пока еще выбираю направление',
                'Нет'
            ],
        }

    async def before(self, payload, data):
        message = "Ты уже подал заявление?"

        buttons = [
            [
                {'text': self.response_phrases['yes'][0]}
            ],
            [
                {'text': self.response_phrases['no'][0]}
            ]
        ]

        keyboard = {
            'keyboard': buttons,
            'resize_keyboard': True,
            'one_time_keyboard': True
        }

        await self.sdk.send_keyboard_to_chat(payload['chat'], message, keyboard)

    async def process(self, payload, data):
        self.sdk.log("State Greeting processor fired with payload {}".format(payload))
        # TODO remove keyboard

        text = payload['text']

        if text in self.response_phrases['yes']:
            # Go to auth
            return await self.controller.goto(payload, 'auth')

        elif text in self.response_phrases['no']:
            message = 'Я могу помочь подобрать направления по твоим результатам ЕГЭ.'

            await self.sdk.send_text_to_chat(
                payload["chat"],
                message
            )

            # Ask scores
            return await self.controller.goto(payload, 'ask_scores')

        message = 'Не понимаю'

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'greeting')
