from . import ApiServer


class Methods:

    @staticmethod
    def check_rating_positions(sdk, student_id):
        ratings = ApiServer().request('getUserPositions', {'id': student_id})

        # todo get user positions from db
        old_position = 19

        sdk.log("RATINGING: {}".format(ratings))
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

            sdk.log("APROGRAM: {}".format(program))

        sdk.log("RATINGING: {}".format(ratings))

        return ratings

    @staticmethod
    def loggy(message='default value'):
        print("Scheduled function with param message: {}".format(message))


