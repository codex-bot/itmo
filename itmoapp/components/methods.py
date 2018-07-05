from . import ApiServer


class Methods:

    def __init__(self, sdk):
        self.sdk = sdk

    def check_rating_positions(self, student_id, payload):
        """
        Check ratings positions update for target student

        :param string student_id:
        :param payload:
        :return list ratings:
        """
        from models import Student

        # Get Student
        student = Student(self.sdk, payload, chat=payload['chat'])

        # if student.programs:

        ratings = ApiServer().request('getUserPositions', {'id': student_id})

        old_position = 19

        for idx, program in enumerate(ratings):
            """
            {
                'program': 'Прикладная и компьютерная оптика',
                'id': 10555,
                'position': 13,
                'users': 67,
                'value': 120
            }
            """

            # todo compare positions with saved in db
            program['position_diff'] = old_position - program['position']

            ratings[idx] = program

            self.sdk.log("APROGRAM: {}".format(program))

        self.sdk.log("RATINGING: {}".format(ratings))

        # todo update user's saved programs

        student.programs = ratings
        student.save()

        return ratings

    async def loggy(self, payload):
        self.sdk.log("Scheduled function loggy() with payload {}".format(payload))
        message = "[daily report]"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )
