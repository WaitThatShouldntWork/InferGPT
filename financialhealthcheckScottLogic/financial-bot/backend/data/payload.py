class BaseMessage(dict):
    def __init__(self, message : str, sender : str):
        dict.__init__(self, message = message, sender = sender)
        self.message = message
        self.sender = sender

class Message(BaseMessage):
    def __init__(self, _id : str, message : str, sender : str, direction: str ):
        dict.__init__(self, id = id, message = message, sender = sender, direction = direction)
        self._id = _id
        self.direction = direction
        super().__init__(message=message, sender=sender)

class ChatReply(BaseMessage):    
    def __init__(self, id:int, message : str, sender : str, originalQuestion:str, dbAnswer:str, userAnswer:str):
        dict.__init__(self, _id = id, message = message, sender = sender, originalQuestion = originalQuestion, dbAnswer = dbAnswer, userAnswer = userAnswer)
        self.originalQuestion = originalQuestion
        self.dbAnswer = dbAnswer
        self.userAnswer = userAnswer
        self._id = id
        super().__init__(message=message, sender=sender)

class RequestPayload:
    def __init__(self, message : Message, sessionId : str):
        self.message = message
        self.sessionId = sessionId

class ResponsePayload:
    def __init__(self, message : Message, userId: int = None, goalId: int = None, sessionId : str = None):
        self.message = message
        self.userId = userId
        self.goalId = goalId
        self.sessionId = sessionId