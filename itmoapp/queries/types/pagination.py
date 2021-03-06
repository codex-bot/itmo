from queries.base import Base
from queries.message import Message


class QueryTypePagination(Base):

    def __init__(self, sdk):
        super().__init__(sdk)

        self.limit_per_page = 5

    @staticmethod
    def name():
        return 'pagination'

    async def create(self, payload, data):
        """
        Send a new message

        :param payload:
        :param data:
        :return:
        """
        # Prepare Type's data
        self.wrapped_data = self.__wrap_data(data)

        # Create a new Message
        self.message = Message(self.sdk)
        self.message.create(self.wrapped_data, self.name())

        # Compose text
        text = self.__generate_text(self.wrapped_data['data'])

        # Create a keyboard
        keyboard = self.__generate_keyboard(1, self.wrapped_data['total_pages'])

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            text,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
            want_response=self.message.hash,
            bot=payload.get('bot', None)
        )

    async def process(self, payload, requested_page):
        """

        :param payload:
        :param requested_page: page number
        :return:
        """
        # Parse page number
        requested_page = int(requested_page)

        # Get text to send
        text = self.__generate_text(self.message.data['data'], requested_page)

        # Generate keyboard
        keyboard = self.__generate_keyboard(requested_page, self.message.data['total_pages'])

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            text,
            keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
            update_id=self.message.id,
            bot=payload.get('bot', None)
        )

    def __wrap_data(self, data):
        """
        Add additional information from this Type and return wrapped data

        :param data:
        :return:
        """
        return {
            "total_pages": self.__count_chunks(data),
            "data": data
        }

    def __count_chunks(self, data):
        """
        Count number of chunks (pages)

        :param data:
        :return number:
        """
        # To get result of divison rounded up we can use div for negative number and multiply it to -1 back
        return ((-1 * data.__len__()) // self.limit_per_page) * -1

    def __generate_text(self, data, page=1):
        text = ''

        # Count number of list items to skip
        skip = (page - 1) * self.limit_per_page

        # Compose message
        for text_block in data[skip:skip + self.limit_per_page]:
            text += text_block

        return text

    def __generate_keyboard(self, cursor, total, keys_per_row=5):
        """
        Generates a keyboard for a current page

        :param number cursor: number of current page
        :param number total: total number of pages
        :param number keys_per_row: number of keys in a row. should be between 5 and 8
        :return list:
        """
        # Prepare array of buttons
        keyboard_row = []

        # For one page we no need to add keyboard
        if total <= 1:
            pass

        # No need to add overjump buttons (with arrow)
        # If count of pages is not greater that the max number of buttons
        #
        # For only 3 pages and 5 max buttons
        # [ 1 ] [ 2 ] [ •3• ]
        # Get pages from
        #   1                   start of the list
        # to
        #   total + 1           because range() does not get right side of interval
        elif total <= keys_per_row:
            for i in range(1, total + 1):
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

            # Okay. Page is not on the sides of pages list
            else:
                # Add the first button with arrow for overjumping
                #
                # [ « 1 ] ...
                keyboard_row.append({
                    "text": "« {}".format(1),
                    "callback_data": self.message.wrap_callback_data(1)
                })

                # Getting adjacent buttons without arrows from
                #   cursor                      current cursor position
                #   - (keys_per_row - 2) // 2   a half of number of buttons left to add
                #   + (keys_per_row + 1) % 2    if number of buttons is even then "center" will be one
                #                               of the first half buttons. then we no need one more step
                #   ... [ _12_ ] [ _13_ ] [ •14• ] [ ... ] [ ... ] ...
                #   ... [ _12_ ] [ _13_ ] [ •14• ] [ ... ] [ ... ] [ ... ] ...
                # to
                #   cursor                      current cursor position
                #   (keys_per_row - 2) // 2     add a half of number of buttons left to add
                #    + 1                        because range() does not get right side of interval
                #   ... [ ... ] [ ... ] [ •14• ] [ _15_ ] [ _16_ ] ...
                #   ... [ ... ] [ ... ] [ •13• ] [ _14_ ] [ _15_ ] [ _16_ ] ...
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
