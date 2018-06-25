from config import API_SERVER_URI
import requests


class ApiServer:

    def __init__(self):
        self.uri = API_SERVER_URI

    def request(self, method, params=None):
        r = requests.get(
            "{}/{}".format(self.uri, method),
            params=params
        )

        # Response should be in JSON format
        response = r.json()

        # Response should contain 'data' field
        return response["data"]
