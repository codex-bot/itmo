from .base import Base
from components import Utils, ApiServer
from models import Student


class StateSettings(Base):

    async def before(self, payload, data):
        # todo
        message = "Настройки пока недоступны"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True,
            bot=payload.get('bot', None)
        )

        await self.controller.process(payload, data)

    async def process(self, payload, data):
        # todo
        # message = "Я подобрал несколько направлений, куда у тебя есть возможность поступить.\n" \
        #           "Для возврата в меню нажми /itmo_start."
        #
        # await self.sdk.send_text_to_chat(
        #     payload["chat"],
        #     message
        # )
        #
        # # Prepare data
        # programs_data = []
        #
        # # Prepate text for each program
        # for program in data:
        #     # Compose link
        #     link = "http://abit.ifmo.ru/program/{}/".format(program['id'])
        #
        #     program_requests = "{} {}".format(
        #         program['requests'],
        #         Utils.endings(int(program['requests']), "заявление", "заявления", "заявлений")
        #     )
        #
        #     program_value = "{} {}".format(
        #         program['value'],
        #         Utils.endings(int(program['value']), "место", "места", "мест")
        #     )
        #
        #     program_message = "<a href=\"{}\">{}</a>\n" \
        #                       "Проходной балл: {}\n" \
        #                       "{} на {}\n" \
        #                       "\n".format(
        #                             link,
        #                             program['name'],
        #                             program['score'],
        #                             program_requests,
        #                             program_value
        #                         )
        #
        #     programs_data.append(program_message)
        #
        # # Send message with buttons
        # await self.queries.create(payload, programs_data, 'pagination')

        # Go to start
        await self.controller.goto(payload, "menu")

