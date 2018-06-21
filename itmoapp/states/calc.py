from .base import Base
from components import Utils


class StateCalc(Base):

    async def before(self, payload, data):
        # todo get user's score from db

        message = "Минутку."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

        # todo send api request

    async def process(self, payload, data):
        message = "Я подобрал несколько направлений, куда у тебя есть возможность поступить."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )

        # todo add list with pages

        programs = [
            {
                "name": "Информатика и программирование",
                "id": "10555",
                "score": "309",
                "requests": "391",
                "value": "121"
            },
            {
                "name": "Прикладная и компьютерная оптика",
                "id": "10565",
                "score": "235",
                "requests": "102",
                "value": "26"
            },
            {
                "name": "Лазеры для информационно-коммуникационных систем",
                "id": "10569",
                "score": "239",
                "requests": "90",
                "value": "25"
            },
            {
                "name": "Физика наноструктур",
                "id": "10566",
                "score": "257",
                "requests": "15",
                "value": "13"
            },
            {
                "name": "Вычислительные системы и сети",
                "id": "10556",
                "score": "272",
                "requests": "165",
                "value": "52"
            },
        ]

        message = ""

        for program in programs:

            link = "http://abit.ifmo.ru/program/{}/".format(program['id'])

            program_requests = "{} {}".format(
                program['requests'],
                Utils.endings(
                    int(program['requests']),
                    "заявление",
                    "заявления",
                    "заявлений"
                )
            )

            program_value = "{} {}".format(
                program['value'],
                Utils.endings(
                    int(program['value']),
                    "место",
                    "места",
                    "мест"
                )
            )
            program_message = "<a href=\"{}\">{}</a>\n" \
                              "Проходной балл: {}\n" \
                              "{} на {}\n" \
                              "\n".format(
                                    link,
                                    program['name'],
                                    program['score'],
                                    program_requests,
                                    program_value
                                )

            message += program_message

        keyboard = [
            [
                {
                    "text": "1",
                    "callback_data": "1"
                },
                {
                    "text": "2",
                    "callback_data": "2"
                },
                {
                    "text": "3",
                    "callback_data": "3"
                },
                {
                    "text": "4",
                    "callback_data": "4"
                },
                {
                    "text": "5",
                    "callback_data": "5"
                },
                {
                    "text": ">",
                    "callback_data": ">"
                },
            ],
        ]

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            message,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        await self.controller.goto(payload, "start")

