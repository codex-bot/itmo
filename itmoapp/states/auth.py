from .base import Base


class StateAuth(Base):

    async def before(self, payload, data):
        message = "Введи номер заявления"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message,
            remove_keyboard=True
        )

    async def process(self, payload, data):
        self.sdk.log("State Start processor fired with payload {}".format(payload))

        user_id = payload["text"]

        # todo parse user id

        # todo if parsing was failed
            # todo show error message
            # todo goto auth

        # todo api request user
        response_data = {
            "name": "Андрей Федотов",
            "scores": [
                {
                    "subject": "Математика",
                    "score": 89
                },
                {
                    "subject": "Русский язык",
                    "score": 93
                },
                {
                    "subject": "Информатика",
                    "score": 100
                },
                {
                    "subject": "Физика",
                    "score": 67
                }
            ]
        }

        if "name" not in response_data or "scores" not in response_data:
            # Send report to Hawk
            try:
                raise Exception("No \"name\" or \"scores\" param in response data on auth with id:{}".format(user_id))
            except Exception as e:
                self.controller.sdk.hawk.catch()

            message = "Не могу получить информацию об анкете с этим номером."

            await self.sdk.send_text_to_chat(
                payload["chat"],
                message
            )

            return await self.controller.goto(payload, "auth")

        # Add user_id to save it
        response_data['id'] = user_id

        # Ask user if returned data is right
        return await self.controller.goto(payload, "ask_auth_correctness", response_data)
