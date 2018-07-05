from .base import Base
from components import Methods, Utils


class StateRatings(Base):

    async def before(self, payload, data):
        message = "Минутку."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        await self.controller.process(payload, data)

    async def process(self, payload, data):

        message = "Список направлений, куда ты подал документы на поступление"

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
                Utils.endings(int(program['value']), "место", "места", "мест")
            )

            chance = int(float(program['value']) / float(program['position']) * 100)

            if program['position_diff'] > 0:
                diff = "+{} 👍".format(program['position_diff'])
            elif program['position_diff'] < 0:
                diff = "{} 👎".format(program['position_diff'])
            else:
                diff = "+0"

            program_message = "<a href=\"{}\">{}</a>\n".format(link, program['program']) + \
                              "Вероятность поступления: {}% {}\n".format(chance, Utils.satisfaction_emoji(chance)) + \
                              "Твое заявление {} ({}) из {} в рейтинге на {}\n".format(program['position'], diff, program['users'], program_value) + \
                              "\n"

            programs_data.append(program_message)

        # Send message with buttons
        await self.queries.create(payload, programs_data, 'pagination')

        message = "Для возврата в меню нажми /itmo_start."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )

        # Go to start
        await self.controller.goto(payload, "start")

