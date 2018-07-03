from .base import CommandBase
from components import Utils
from config import USERS_COLLECTION_NAME


class CommandStart(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/itmo_start handler fired with payload {}".format(payload))

        # Save user to db
        self.save_to_db(payload)

        # Go to state START
        await self.state.goto(payload, 'start')

        # Run process function for current state (start)
        await self.state.process(payload)

    def save_to_db(self, payload):
        """
        Save user to db

        :param payload:
        :return:
        """
        # Upsert chat to db
        self.sdk.db.update(
            # Collection name
            Utils.create_collection_name(USERS_COLLECTION_NAME, payload),

            # Find params
            {'chat': payload['chat']},

            # Data to be saved
            {'chat': payload['chat']},

            # Upsert = true
            True
        )
