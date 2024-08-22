
import logging
from flask import session

from utilities.defaults import Defaults
class SessionManager:
    @staticmethod
    def getSessionValue(sessionId, key):
        if session.get(sessionId) is not None:
            if key in session[sessionId]:
                return session[sessionId][key]
        return None

    @staticmethod
    def saveSessionValue(sessionId, key, val):
        if session.get(sessionId) is None:
            session[sessionId] = {}
        session[sessionId][key] = val
        session.modified = True

    @staticmethod
    def storeSessionData(sessionId, userIdVal, conversationIdVal, goalIdVal):
        logger = logging.getLogger('chatBot')
        logger.debug(f"called storeSessionData {sessionId=} {userIdVal=} {conversationIdVal=} {goalIdVal=})")
        SessionManager.saveSessionValue(sessionId, Defaults.userIdSessionKey, userIdVal)
        SessionManager.saveSessionValue(sessionId, Defaults.goalIdSessionKey, goalIdVal)
        SessionManager.saveSessionValue(sessionId, Defaults.conversationIdSessionKey, conversationIdVal)