from .base import Base
from components import Utils, ApiServer
import json


class StateCalc(Base):

    async def before(self, payload, data):
        message = "Минутку."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

        self.sdk.log("Scores: {}".format(data))

        programs = ApiServer().request('getProgramsByScores', {"scores": json.dumps(data)})
        self.sdk.log("API Server response for getProgramsByScores: {}".format(programs))

        await self.controller.process(payload, programs)

    async def process(self, payload, data):
        message = "Я подобрал несколько направлений, куда у тебя есть возможность поступить.\n" \
                  "Для возврата в меню нажми /itmo_start."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
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
                Utils.endings(int(program['value']), "место", "места", "мест")
            )

            chance = int(float(program['value']) / float(program['possible_place']) * 100)

            program_message = "<a href=\"{}\">{}</a>\n".format(link, program['name']) + \
                              "Проходной балл: {}\n".format(program['score']) + \
                              "Вероятность поступления: {}% {}\n".format(chance, Utils.satisfaction_emoji(chance)) + \
                              "Твое заявление было бы {} из {} в рейтинге на {}\n".format(program['possible_place'], program['requests'], program_value) + \
                              "\n"

            programs_data.append(program_message)

        # Send message with buttons
        await self.queries.create(payload, programs_data, 'pagination')

        # Go to start
        await self.controller.goto(payload, "start")

