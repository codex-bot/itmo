from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER
from commands.requests import CommandRequests
from commands.start import CommandStart
from commands.login import CommandLogin

class Ifmo:

    def __init__(self):
        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Ifmo module initialized")

        self.sdk.register_commands([
            ('ifmo_requests', 'requests', CommandRequests(self.sdk)),
            ('ifmo_start', 'start', CommandStart(self.sdk)),
            ('ifmo_login', 'login', CommandLogin(self.sdk))
        ])

        self.sdk.start_server()

if __name__ == "__main__":
    ifmo = Ifmo()
