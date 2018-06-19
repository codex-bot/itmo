from .base import Base


class StateAskScores(Base):


    # def __init__(self, state_controller):
    #     super().__init__(state_controller)

        # self.response_phrases = {
        #     'ratings': [
        #         'Позиции в рейтингах'
        #     ],
        #
        #     'EGE_calc': [
        #         'Подобрать направления по баллам'
        #     ],
        #
        #     'notifications': [
        #         'Настроить оповещения'
        #     ],
        #
        #     'logout': [
        #         'Выйти из системы'
        #     ],
        # }
    async def before(self, payload, data):
        message = "Пришли мне список своих баллов в формате:\n" \
                  "\n" \
                  "Математика 80\n" \
                  "Русский язык 78\n" \
                  "Информатика 65"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

    async def process(self, payload, data):
        self.sdk.log("State Menu processor fired with payload {}".format(payload))

        text = payload['text']

        # TODO parse user's scores

        # TODO if parse was successful
            # save data to DB (?)

            # goto calc with this data
        return await self.controller.goto(payload, 'calc')





        # if text in self.response_phrases['ratings']:
        #     pass
        # elif text in self.response_phrases['EGE_calc']:
        #     pass
        # elif text in self.response_phrases['notifications']:
        #     pass
        # elif text in self.response_phrases['logout']:
        #     pass
        # else:
        #     self.sdk.log("PHRASE IS UNDEFINED")

        message = 'Не могу разобрать '

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        return await self.controller.goto(payload, 'ask_scores')
