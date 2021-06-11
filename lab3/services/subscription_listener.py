from threading import Thread

from db.redis_connection import red
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
        messages_listener = red.pubsub()
        messages_listener.subscribe(['login', 'logout', 'spam'])

        for ev in messages_listener.listen():
            try:
                if ev['type'] == 'message':
                    self.eventToCallback[ev['channel']]()
            except:
                continue
