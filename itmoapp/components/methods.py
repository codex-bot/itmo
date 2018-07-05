from . import ApiServer


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

    async def loggy(self, payload):
        self.sdk.log("Scheduled function loggy() with payload {}".format(payload))
        message = "[daily report]"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            bot=payload.get('bot', None)
        )
