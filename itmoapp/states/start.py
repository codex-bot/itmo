from .base import Base


class StateStart(Base):

    async def process(self, payload, data):
        # if user is autorized: TODO check if user is authorized
        #     return await self.controller.goto(payload, 'menu')

        # User is not autorized
        message = "Привет. Я буду держать тебя в курсе твоего состояния поступления в ИТМО."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'greeting')
