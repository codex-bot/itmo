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
        text = self.__generate_text(1)

        # todo create keyboard
        keyboard = self.__generate_keyboard(1, 50)

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

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            text,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
            update_id=self.message.id
        )

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
        # Should be between 5 and 8
        keys_per_row = 5

        keyboard_row = []

        # For one page we no need to add keyboard
        if total == 1:
            pass

        # No need to add overjump buttons (with arrow)
        # If count of pages is not greater that the max number of buttons
        #
        # For only 3 pages and 5 max buttons
        # [ 1 ] [ 2 ] [ •3• ]
        elif total <= keys_per_row:
            for i in range(1, keys_per_row + 1):
                keyboard_row.append({
                    "text": i if i != cursor else "• {} •".format(i),
                    "callback_data": self.message.wrap_callback_data(i)
                })

        # We need to add overjumps
        else:
            # Find a center button
            #
            # For 5 (odd)
            # [ ] [ ] [X] [ ] [ ]
            #
            # For 6 (even)
            # [ ] [ ] [X] [ ] [ ] [ ]
            half_of_keys_per_row = keys_per_row // 2 + keys_per_row % 2

            # If this page in the start of pages list
            #
            # If current page is not grater than a half of keys per row
            #
            # [ 1 ] [ 2 ] [ •3• ] [ 4 ] [ 5 ] [ 16 » ]
            if cursor <= half_of_keys_per_row:
                # Get pages from
                #   1                   start of the list
                # to
                #   keys_per_row - 1    max number of buttons minus button with arrow
                #   + 1                 because range() does not get right side of interval
                for i in range(1, (keys_per_row - 1) + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

                # Add the last button with arrow for overjumping
                #
                # ... [ 50 » ]
                keyboard_row.append({
                    "text": "{} »".format(total),
                    "callback_data": self.message.wrap_callback_data(total)
                })

            # Check if his page in the end part of the list
            #
            # If the page number belongs the last half_of_keys_per_row of the list
            elif cursor > total - half_of_keys_per_row:
                # Add the first button with arrow for overjumping
                #
                # [ « 1 ] ...
                keyboard_row.append({
                    "text": "« {}".format(1),
                    "callback_data": self.message.wrap_callback_data(1)
                })

                # Get pages from
                #   total - keys_per_row + 1    last keys_per_row elements of the list (count from 1)
                #   + 1                         we have placed for the first button with arrow
                # to
                #   total + 1                   because range() does not get right side of interval
                #
                # For 47th page of 50 with 6 buttons
                # [ « 1 ] [ 46 ] [ •47• ] [ 48 ] [ 49 ] [ 50 ]
                for i in range((total - keys_per_row + 1) + 1, total + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

            else:
                # Add the first button with arrow for overjumping
                #
                # [ « 1 ] ...
                keyboard_row.append({
                    "text": "« {}".format(1),
                    "callback_data": self.message.wrap_callback_data(1)
                })

                
                for i in range(cursor - ((keys_per_row - 2) // 2) + (keys_per_row + 1) % 2, cursor + ((keys_per_row - 2) // 2) + 1):
                    keyboard_row.append({
                        "text": i if i != cursor else "• {} •".format(i),
                        "callback_data": self.message.wrap_callback_data(i)
                    })

                # Add the last button with arrow for overjumping
                #
                # ... [ 50 » ]
                keyboard_row.append({
                    "text": "{} »".format(total),
                    "callback_data": self.message.wrap_callback_data(total)
                })

        # Add keyboard_row to keyboard
        keyboard = [
            keyboard_row
        ]

        return keyboard

    def __generate_text(self, data):
        text = ''

        text = 'data on page {}'.format(data)

        return text
