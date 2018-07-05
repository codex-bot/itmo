from .base import Base
from components import Methods, Utils


class StateRatings(Base):

    async def before(self, payload, data):
        message = "Минутку"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        await self.controller.process(payload, data)

    async def process(self, payload, data):

        message = "Список направлений, куда вы подали документы на поступление"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        ratings = Methods(self.sdk).check_rating_positions(payload)
        self.sdk.log("API Server response for getUserPositions: {}".format(ratings))

        # Prepare data
        programs_data = []

        # Prepare text for each program
        for program_id, program in ratings.items():
            # Compose link
            link = "http://abit.ifmo.ru/program/{}/".format(program_id)

            program_value = "{} {}".format(
                program['value'],
                Utils.endings(
                    int(program['value']),
                    "бюджетное место",
                    "бюджетных места",
                    "бюджетных мест"
                )
            )

            chance = int(float(program['value']) / float(program['position']) * 100)

            if program['position_diff'] > 0:
                diff = "+{} 👍".format(program['position_diff'])
            elif program['position_diff'] < 0:
                diff = "{} 🔻".format(program['position_diff'])
            else:
                diff = None

            program_message = "<a href=\"{}\">{}</a>\n".format(link, program['program']) + \
                              "Вероятность поступления: {}% {}\n".format(chance, Utils.satisfaction_emoji(chance)) + \
                              "Ваше заявление {}{} из {}.\n".format(
                                  program['position'],
                                  " ({})".format(diff) if diff else "",
                                  program['users']
                              ) + \
                              "{}\n".format(program_value) + \
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

