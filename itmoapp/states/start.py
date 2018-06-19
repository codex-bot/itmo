from .base import Base
from itmoapp.models import Student


class StateStart(Base):

    async def process(self, payload, data):
        student = Student(self.sdk, chat=payload['chat'])

        if student.get('name') is not None:
             return await self.controller.goto(payload, 'menu')

        # User is not autorized
        message = "Привет. Я буду держать тебя в курсе твоего состояния поступления в ИТМО."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'greeting')
