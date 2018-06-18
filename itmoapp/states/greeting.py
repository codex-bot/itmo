from .base import Base


class StateGreeting(Base):

    async def before(self, payload):
        message = "Привет. Я буду держать тебя в состояния поступления в ИТМО.\n" \
                  "Ты уже подал заявление?"

        buttons = [
            [
                {'text': 'Да, у меня уже есть номер'}
            ],
            [
                {'text': 'Нет, пока еще выбираю направление'}
            ]
        ]

        keyboard = {
            'keyboard': buttons,
            'resize_keyboard': True,
            'one_time_keyboard': True
        }

        await self.sdk.send_keyboard_to_chat(payload['chat'], message, keyboard)

    async def process(self, payload):
        self.sdk.log("State Start processor fired with payload {}".format(payload))
        # TODO remove keyboard

        text = payload['text']

        if text == "Да, у меня уже есть номер":
            return await self.controller.goto(payload, 'auth')
        elif text == "Нет, пока еще выбираю направление":
            pass
        else:
            pass

        message = 'я могу помочь ...'

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'start')
