class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
class Question:
    def __init__(self, questionId, question, intent = None, answer = None):
        self.questionId = questionId
        self.question = question
        self.intent = intent
        self.answer = answer
        self.originalQuestion = question