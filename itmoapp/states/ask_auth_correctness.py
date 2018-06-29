from .base import Base
from models import Student
from components import Methods

class StateAskAuthCorrectness(Base):

    def __init__(self, state_controller):
        super().__init__(state_controller)

        self.response_phrases = {
            "yes": [
                "Да"
            ],

            "no": [
                "Нет"
            ],
        }

    async def before(self, payload, data):
        user_name = data["name"] if "name" in data else None

        # User name is missing
        if user_name is None:
            # message = "Не могу найти твое имя в анкете"
            #
            # await self.sdk.send_text_to_chat(
            #     payload["chat"],
            #     message
            # )

            # Go back to auth state
            return await self.controller.goto(payload, "auth")

        message = "Тебя зовут {}?".format(user_name)

        buttons = [
            [
                {"text": self.response_phrases["yes"][0]},
                {"text": self.response_phrases["no"][0]}
            ]
        ]

        keyboard = {
            "keyboard": buttons,
            "resize_keyboard": True,
            "one_time_keyboard": True
        }

        await self.sdk.send_keyboard_to_chat(payload["chat"], message, keyboard)

    async def process(self, payload, data):
        self.sdk.log("State AskAuthCorrectness processor fired with payload {}".format(payload))
        # TODO remove keyboard

        text = payload["text"]

        # If user answer "yes, it"s me"
        if text in self.response_phrases["yes"]:
            student = Student(self.sdk, data={
                "chat": payload["chat"],
                "id": data["id"],
                "name": data["name"],
                "scores": data["scores"]
            }).save()

            # Add checking for User's positions in ratings
            self.sdk.log("Scheduler for chat {} was added".format(payload['chat']))
            self.sdk.scheduler.add(
                Methods.loggy,
                chat_id=payload["chat"],
                args=[],    # todo set up args
                trigger_params={'hour': '21'}
            )

            # Go to menu
            return await self.controller.goto(payload, "menu")

        # If user answer "no"
        message = "Попробуй авторизоваться еще раз."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, "auth")