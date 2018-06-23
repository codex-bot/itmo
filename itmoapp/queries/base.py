class Base:

    def __init__(self, sdk):
        self.sdk = sdk

        self.wrapped_data = {}
        self.message = None

    @staticmethod
    def name():
        return ''

    def create(self, payload, data):
        pass

    def process(self, payload, data):
        pass

    def __wrap_data(self, data):
        pass
