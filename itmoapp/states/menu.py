from .base import Base
from models import Student


class StateMenu(Base):
    """
    Show menu with actions for authorized users
    """

    def __init__(self, state_controller):
        super().__init__(state_controller)

        self.response_phrases = {
            "ratings": [
                "Мои позиции в рейтингах"
            ],

            "EGE_calc": [
                "Подобрать направления по баллам"
            ],

            "notifications": [
                "Настроить оповещения"
            ],

            "logout": [
                "Выйти из системы"
            ],
        }

    async def before(self, payload, data):
        message = "Что тебя интересует?"

        buttons = [
            [
                {"text": self.response_phrases["ratings"][0]}
            ],
            [
                {"text": self.response_phrases["EGE_calc"][0]}
            ],
            # [
            #     {"text": self.response_phrases["notifications"][0]}
            # ],
            [
                {"text": self.response_phrases["logout"][0]}
            ]
        ]

        keyboard = {
            "keyboard": buttons,
            "resize_keyboard": True,
            "one_time_keyboard": True
        }

        await self.sdk.send_keyboard_to_chat(payload["chat"], message, keyboard)

    async def process(self, payload, data):
        self.sdk.log("State Menu processor fired with payload {}".format(payload))

        text = payload["text"]

        if text in self.response_phrases["EGE_calc"]:
            student = Student(self.sdk, chat=payload['chat'])

            scores = student.scores

            # Show programs for user by scores
            return await self.controller.goto(payload, "calc", scores)

        elif text in self.response_phrases["ratings"]:
            return await self.controller.goto(payload, "ratings")

        # elif text in self.response_phrases["notifications"]:
        #     return await self.controller.goto(payload, "settings")

        elif text in self.response_phrases["logout"]:
            # Remove student data from database
            Student(self.sdk, chat=payload["chat"]).remove()

            # Remove checking for User's positions in ratings
            self.sdk.log("Scheduler for chat {} was removed".format(payload['chat']))
            self.sdk.scheduler.remove(payload['chat'])

            # Send message
            message = "Если понадоблюсь, выполни команду /itmo_start."

            await self.sdk.send_text_to_chat(
                payload["chat"],
                message,
                remove_keyboard=True
            )

            # Go to start state
            return await self.controller.goto(payload, "start")

        # Response to undefined user reply
        message = "Не понимаю"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

        return await self.controller.goto(payload, "menu")
