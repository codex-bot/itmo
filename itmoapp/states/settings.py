from .base import Base
from components import Utils, ApiServer
from models import Student


class StateSettings(Base):

    async def before(self, payload, data):
        # todo
        message = "Настройки пока недоступны"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        await self.controller.process(payload, data)

    async def process(self, payload, data):
        # todo

        # Go to start
        await self.controller.goto(payload, "menu")

