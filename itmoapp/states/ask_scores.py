from .base import Base


class StateAskScores(Base):

    async def before(self, payload, data):
        message = "Пришли мне список своих баллов в формате:\n" \
                  "\n" \
                  "Математика 80\n" \
                  "Русский язык 78\n" \
                  "Информатика 65"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

    async def process(self, payload, data):
        self.sdk.log("State Menu processor fired with payload {}".format(payload))

        text = payload["text"]

        # TODO parse user's scores

        # TODO if parse was successful
        if True:
            # save data to DB (?)

            # goto calc with this data
            await self.controller.goto(payload, "calc")
            return await self.controller.process(payload)

        # Ask resend scores again
        message = "Не могу разобрать"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, "ask_scores")
