from .base import Base
from components import Utils, ApiServer
import json


class StateCalc(Base):

    async def before(self, payload, data):
        message = "Минутку"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        self.sdk.log("Scores: {}".format(data))

        programs = ApiServer().request('getProgramsByScores', {"scores": json.dumps(data)})
        self.sdk.log("API Server response for getProgramsByScores: {}".format(programs))

        await self.controller.process(payload, programs)

    async def process(self, payload, data):
        message = "Я подобрал несколько направлений, куда у вас есть возможность поступить."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        # Prepare data
        programs_data = []

        # Prepare text for each program
        for program in data:
            # Compose link
            link = "http://abit.ifmo.ru/program/{}/".format(program['id'])

            # program_requests = "{} {}".format(
            #     program['requests'],
            #     Utils.endings(int(program['requests']), "заявление", "заявления", "заявлений")
            # )

            program_value = "{} {}".format(
                program['value'],
                Utils.endings(
                    int(program['value']),
                    "бюджетное место",
                    "бюджетных места",
                    "бюджетных мест"
                )
            )

            chance = min(int(float(program['value']) / float(program['possible_place']) * 100), 100)

            program_message = "<a href=\"{}\">{}</a>\n".format(link, program['name']) + \
                              "Проходной балл: {}\n".format(program['score']) + \
                              "Ваше заявление было бы {} из {}\n".format(
                                  program['possible_place'],
                                  program['requests']
                              ) + \
                              "{}\n".format(
                                  program_value
                              ) + \
                              "Вероятность поступления: {}% {}\n".format(chance, Utils.satisfaction_emoji(chance)) + \
                              "\n"

            programs_data.append(program_message)

        # Send message with buttons
        await self.queries.create(payload, programs_data, 'pagination')

        message = "Нажмите /itmo_start для возврата в меню"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        # Go to start
        await self.controller.goto(payload, "start")

