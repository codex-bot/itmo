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

        # todo api request

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
            {
                "name": "Программирование и интернет-технологии",
                "id": "10557",
                "score": "300",
                "requests": "400",
                "value": "90"
            },
            {
                "name": "Системное и прикладное программное обеспечение",
                "id": "10558",
                "score": "283",
                "requests": "89",
                "value": "80"
            },
            {
                "name": "Компьютерные технологии в дизайне",
                "id": "10559",
                "score": "283",
                "requests": "101",
                "value": "14"
            },
            {
                "name": "Нейротехнологии и программирование",
                "id": "10559",
                "score": "282",
                "requests": "100",
                "value": "20"
            },
        ]

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

        # Prepate text for each program
        for program in data:
            # Compose link
            link = "http://abit.ifmo.ru/program/{}/".format(program['id'])

            program_requests = "{} {}".format(
                program['requests'],
                Utils.endings(int(program['requests']), "заявление", "заявления", "заявлений")
            )

            program_value = "{} {}".format(
                program['value'],
                Utils.endings(int(program['value']), "место", "места", "мест")
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

            programs_data.append(program_message)

        # Send message with buttons
        await self.queries.create(payload, programs_data, 'pagination')

        # Go to start
        await self.controller.goto(payload, "start")

