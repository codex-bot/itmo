from queries.base import Base
from queries.message import Message


class QueryTypePagination(Base):

    def __init__(self, sdk):
        super().__init__(sdk)

        self.limit_per_page = 3

    @staticmethod
    def name():
        return 'pagination'

    async def create(self, payload, data):
        """
        Send a new message

        :return:
        """
        self.sdk.log("payload {}".format(payload))
        self.sdk.log("data {}".format(data))

        self.wrapped_data = self.__wrap_data(data)
        self.message = Message(self.sdk)
        self.message.create(self.wrapped_data, self.name())

        self.sdk.log("Message {} was CREATED as {}".format(self.wrapped_data, self.name()))

        # todo create text
        text = self.__generate_text()

        # todo create keyboard
        keyboard = self.__generate_keyboard(2, 50)

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            text,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
            want_response=self.message.hash
        )

    async def process(self, payload, data):

        # todo create text
        text = self.__generate_text(data)

        # todo create keyboard
        keyboard = self.__generate_keyboard(int(data), 50)

        # keyboard = [
        #     [
        #         {
        #             "text": int(callback_data["data"]) - 2,
        #             "callback_data": message.wrap_callback_data(int(callback_data["data"]) - 2)
        #         },
        #         {
        #             "text": int(callback_data["data"]) - 1,
        #             "callback_data": message.wrap_callback_data(int(callback_data["data"]) - 1)
        #         },
        #         {
        #             "text": int(callback_data["data"]),
        #             "callback_data": message.wrap_callback_data(int(callback_data["data"]))
        #         },
        #         {
        #             "text": int(callback_data["data"]) + 1,
        #             "callback_data": message.wrap_callback_data(int(callback_data["data"]) + 1)
        #         },
        #         {
        #             "text": int(callback_data["data"]) + 2,
        #             "callback_data": message.wrap_callback_data(int(callback_data["data"]) + 2)
        #         },
        #     ],
        # ]

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            text,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
            update_id=self.message.id
        )

        # await self.sdk.send_inline_keyboard_to_chat(
        #     payload["chat"],
        #     "Давай, пидрила, листай дальше",
        #     keyboard,
        #     update_id=message.id,
        # )

    def __wrap_data(self, data):
        """
        Return wrapped data

        :param data:
        :return:
        """
        return {
            'data': data
        }

    def __generate_keyboard(self, cursor, total):
        """
        Generate keyboard for a current page

        [1] [2] [3] [4] [50]
        [1] [14] [15] [16] [50]
        [1] [2] [3]

        :param cursor:
        :param total:
        :return:
        """
        # Should be between 4 and 8
        keys_per_row = 7

        keyboard_row = []

        # keys_left = min(5, total)

        # No need to add keyboard
        if total == 1:
            pass

        # No need to add overjump (arrows) buttons
        #
        # For only 3 pages:
        # [ 1 ] [ 2 ] [ •3• ]
        elif total <= keys_per_row:
            for i in range(1, keys_per_row + 1):
                keyboard_row.append({
                    "text": i if i != cursor else "• {} •".format(i),
                    "callback_data": self.message.wrap_callback_data(i)
                })

        # Need to add overjumps
        else:
            # If this page in the start of pages list
            #
            # [ 1 ] [ 2 ] [ •3• ] [ 4 ] [ 14 » ]
            if cursor < keys_per_row // 2 + 1 + (keys_per_row % 2):
                for i in range(1, (keys_per_row - 1) + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

                keyboard_row.append({
                    "text": "{} »".format(total),
                    "callback_data": self.message.wrap_callback_data(total)
                })

            #
            elif cursor > total - (keys_per_row // 2) - 1 + (keys_per_row + 1) % 2:
                keyboard_row.append({
                    "text": "« {}".format(1),
                    "callback_data": self.message.wrap_callback_data(1)
                })

                for i in range((total - keys_per_row + 1) + 1, total + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

            else:
                keyboard_row.append({
                    "text": "« {}".format(1),
                    "callback_data": self.message.wrap_callback_data(1)
                })

                for i in range(cursor - ((keys_per_row - 2) // 2) + (keys_per_row + 1) % 2, cursor + ((keys_per_row - 2) // 2) + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

                keyboard_row.append({
                    "text": "{} »".format(total),
                    "callback_data": self.message.wrap_callback_data(total)
                })

            #
            # keyboard_row.insert(0, {
            #     # todo add arrow if it required
            #     "text": 1,
            #     "callback_data": self.message.wrap_callback_data(1)
            # })
            #
            # keyboard_row.append({
            #     # todo add arrow if it required
            #     "text": total,
            #     "callback_data": self.message.wrap_callback_data(total)
            # })

        keyboard = [
            keyboard_row
        ]

        return keyboard

    def __generate_text(self, data):
        text = ''

        text = 'data on page {}'.format(data)

        return text
