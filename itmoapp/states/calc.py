from .base import Base


class StateCalc(Base):

    async def before(self, payload, data):
        pass

    async def process(self, payload, data):
        message = "Я подобрал несколько направлений, куда у тебя есть возможность поступить"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        message = "- никуда"

        keyboard = [
            [
                {
                    "text": 1,
                    "callback_data": "1"
                },
                {
                    "text": 2,
                    "callback_data": "2"
                },
                {
                    "text": 3,
                    "callback_data": "3"
                },
                {
                    "text": 4,
                    "callback_data": "4"
                },
                {
                    "text": 5,
                    "callback_data": "5"
                },
                {
                    "text": "">"",
                    "callback_data": ">"
                },
            ],
        ]

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            message,
            keyboard
        )

        await self.controller.goto(payload, "start")
