from .base import Base
from components import Methods, Utils


class StateRatings(Base):

    async def before(self, payload, data):
        message = "Минутку"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        await self.controller.process(payload, data)

    async def process(self, payload, data):

        message = "Направления, на которые вы подали документы."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        await Methods(self.sdk).report_ratings(payload)

        message = "Нажмите /itmo_start для возврата в меню"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        # Go to start
        await self.controller.goto(payload, "start")

