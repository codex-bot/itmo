from .base import Base


class StateStart(Base):

    async def process(self, payload):
        # TODO check if user is authorized

        return await self.controller.goto(payload, 'greeting')
