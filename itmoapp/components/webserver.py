from sdk.codexbot_sdk import CodexBot
from config import USERS_COLLECTION_NAME
import aiohttp.web


class Webserver:

    def __init__(self, sdk):
        self.sdk = sdk
        self.public_directory = './webserver/public'

        # Set up routes for http
        self.sdk.set_routes([
            ('GET', '/', self.http_show_form),
            ('POST', '/', self.http_process_form)
        ])

        # Define static files root
        self.sdk.set_path_to_static('/public', self.public_directory)

        # Run http server
        self.sdk.start_server()

    @CodexBot.http_response
    async def http_show_form(self, request):
        """
        Return form for announcement

        :param request:
        :return:
        """
        # Read raw html code
        with open('./webserver/index.html', 'r', encoding="utf-8") as f:
            index_page = f.read()

        # Return html to the page
        return {
            'text': index_page,
            'content-type': 'text/html',
            'status': 200
        }

    async def http_process_form(self, request):
        """
        Process form and redirect to main page

        :param request:
        :return:
        """
        try:
            post = await request.post()

            # Checking for a "confirmation_checkbox" emptying
            if "confirmation_checkbox" not in post or not post["confirmation_checkbox"]:
                return aiohttp.web.HTTPBadRequest(text="Sending was not confirmed")

            # Checking for a "text" field emptying
            if "text" not in post or not post["text"]:
                return aiohttp.web.HTTPBadRequest(text="Can not send empty message")

            all_users = self.sdk.db.find(USERS_COLLECTION_NAME, {})
            for user in all_users:
                await self.sdk.send_text_to_chat(
                    user["chat"],
                    post["text"],
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )

            return aiohttp.web.HTTPFound('/?success=1')
        except Exception as e:
            if self.sdk.hawk:
                self.sdk.hawk.catch()

            # Return 500 error
            return aiohttp.web.HTTPInternalServerError(text=str(e))
