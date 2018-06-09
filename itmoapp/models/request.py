class Request:

    def __init__(self, data):
        self.id = data.get('id', 0)
        self.faculty = data.get('faculty', '')
        self.program = data.get('program', '')
        self.min_score = data.get('min_score', 0)
        self.required_subjects = data.get('required_subjects', [])
