from .base import Base
from models import Student


class StateStart(Base):
    """
    State start is an entry point of the application.
    It checks if user is authorized and routes to menu or greetings state.
    """

    async def process(self, payload, data):
        # Try to get student data for this chat
        student = Student(self.sdk, payload, chat=payload['chat'])

        # If user is authorized then show menu
        if student.name is not None:
            return await self.controller.goto(payload, 'menu')

        # User is not authorized
        message = "Привет. Я буду держать в курсе твоего состояния поступления в ИТМО."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        return await self.controller.goto(payload, 'greeting')
