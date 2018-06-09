class Student:

    def __init__(self, data):
        """

        :param data:
        """
        self.id = data.get('id', 0)
        self.name = data.get('name', '')
        self.test_scores = data.get('test_scores', [])
        self.requests = data.get('requests', [])

    def get_positions(self):
        """

        :return:
        """
        pass