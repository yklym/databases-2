from threading import Thread

from db.redis_connection import r
from services.logger import loggerService


class MessagesListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.eventToCallback = {
            'login': loggerService.login,
            'logout': loggerService.logout,
            'spam': loggerService.spam
        }

    def run(self):
        messages_listener = r.pubsub()
        messages_listener.subscribe(['login', 'logout', 'spam'])

        try:
            for ev in messages_listener.listen():
                if ev['type'] == 'message':
                    self.eventToCallback[ev['channel']]()
        except:
            return
