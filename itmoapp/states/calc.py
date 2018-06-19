from .base import Base


class StateCalc(Base):

    async def before(self, payload, data):
        message = "Я подобрал несколько направлений, куда у тебя есть возможность поступить"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        message = "- никуда"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'start')

    async def process(self, payload, data):
        pass
        # self.sdk.log("State Menu processor fired with payload {}".format(payload))
        #
        # text = payload['text']
        #
        # # TODO parse user's scores
        #
        #
        #
        # # if text in self.response_phrases['ratings']:
        # #     pass
        # # elif text in self.response_phrases['EGE_calc']:
        # #     pass
        # # elif text in self.response_phrases['notifications']:
        # #     pass
        # # elif text in self.response_phrases['logout']:
        # #     pass
        # # else:
        # #     self.sdk.log("PHRASE IS UNDEFINED")
        #
        # # message = 'спасибо. пока'
        # #
        # # await self.sdk.send_text_to_chat(
        # #     payload["chat"],
        # #     message
        # # )
        #
        # return await self.controller.goto(payload, 'start')
