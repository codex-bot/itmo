from .base import CommandBase


class CommandStart(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/ifmo handler fired with payload {}".format(payload))

        # Go to state START
        await self.state.goto(payload, 'start')

        # Run process function for current state
        await self.state.process(payload)
