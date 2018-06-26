from .base import Base
from components import Utils, ApiServer
from models import Student


class StateRatings(Base):

    async def before(self, payload, data):
        message = "Минутку."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

        student = Student(self.sdk, chat=payload['chat'])

        ratings = ApiServer().request('getUserPositions', {'id': student.id})
        self.sdk.log("API Server response for getUserPositions: {}".format(ratings))

        await self.controller.process(payload, ratings)

    async def process(self, payload, data):
        message = "Список направлений, куда ты подал документы на постуление.\n" \
                  "Для возврата в меню нажми /itmo_start."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        # Prepare data
        programs_data = []

        # Prepate text for each program
        for program in data:
            # Compose link
            link = "http://abit.ifmo.ru/program/{}/".format(program['id'])

            program_requests = "{} {}".format(
                program['users'],
                Utils.endings(int(program['users']), "заявление", "заявления", "заявлений")
            )

            program_value = "{} {}".format(
                program['value'],
                Utils.endings(int(program['value']), "место", "места", "мест")
            )

            chance = int(float(program['value']) / float(program['position']) * 100)

            program_message = "<a href=\"{}\">{}</a>\n" \
                              "Подано {} на {}\n" \
                              "Твое заявление {} в рейтинге\n" \
                              "Вероятность поступления: {}% {}\n" \
                              "\n".format(
                                  link,
                                  program['program'],
                                  program_requests,
                                  program_value,
                                  program['position'],
                                  chance,
                                  Utils.satisfaction_emoji(chance)
                              )

            programs_data.append(program_message)

        # Send message with buttons
        await self.queries.create(payload, programs_data, 'pagination')

        # Go to start
        await self.controller.goto(payload, "start")

