from . import ApiServer
import random


class Methods:

    def __init__(self, sdk):
        self.sdk = sdk

    def check_rating_positions(self, payload):
        """
        Check ratings positions update for target student

        :param string student_id:
        :param payload:
        :return list ratings:
        """
        from models import Student

        # Get Student's data from db
        student = Student(self.sdk, payload, chat=payload['chat'])

        # Send request to api server
        ratings = ApiServer().request('getUserPositions', {'id': student.id})

        # Prepare new ratings dictionary
        new_ratings = {}

        for program in ratings:
            """
            {
                'program': 'Прикладная и компьютерная оптика',
                'id': 10555,
                'position': 13,
                'users': 67,
                'value': 120
            }
            """
            program_id = program['id']

            program['position_diff'] = 0

            try:
                # Get user's last position
                last_position = student.programs[str(program_id)]['position']

                program['position_diff'] = last_position - program['position']
            except Exception as e:
                pass

            new_ratings[str(program_id)] = program

        student.programs = new_ratings
        student.save()

        return new_ratings

    async def report_ratings(self, payload):
        from queries import Query
        from components import Utils

        ratings = self.check_rating_positions(payload)
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

            chance = min(int(float(program['value']) / float(program['position']) * 100), 100)

            if program['position_diff'] > 0:
                diff = "+{} ⬆️️".format(program['position_diff'])
            elif program['position_diff'] < 0:
                diff = "{} 🔻".format(program['position_diff'])
            else:
                diff = None

            program_message = "<a href=\"{}\">{}</a>\n".format(link, program['program']) + \
                              "Ваше заявление {} из {}{}.\n".format(
                                  program['position'],
                                  program['users'],
                                  " ({})".format(diff) if diff else ""
                              ) + \
                              "{}\n".format(program_value) + \
                              "Вероятность поступления: {}% {}\n".format(chance, Utils.satisfaction_emoji(chance)) + \
                              "\n"

            programs_data.append(program_message)

        # Send message with buttons
        await Query(self.sdk).create(payload, programs_data, 'pagination')

    async def evening_digest(self, payload):
        self.sdk.log("Run scheduled function evening_digest() with payload {}".format(payload))

        messages = [
            "Вечерний дайджест.",
            "Пришло время для вечернего дайджеста.",
            "Привет. Вот статус ваших заявлений на сегодняшний день.",
            "Информация о поданных заявлениях к этому часу.",
            "Добрейшего вечерочка. Так обстоят дела с вашими заявлениями:",
            "Самое время узнать, как обстоят дела с вашими заявлениями.",
            "По итогам дня ваши заявления имеют такие позиции.",
            "Привет. Посмотрим, что с вашими позициями."
        ]

        await self.sdk.send_text_to_chat(
            payload["chat"],
            random.choice(messages),
            bot=payload.get('bot', None)
        )

        await self.report_ratings(payload)
