from repositories.message import MessageRepository
from random import randint
from time import sleep
from threading import Thread
from services.subscription_listener import MessagesListener

DELAY = randint(0, 2)


class MessageWorker(Thread):
    def __init__(self):
        Thread.__init__(self)
        pass

    def run(self):
        while True:
            message = MessageRepository.get_next_queue_message()
            if message is None:
                continue
            self.process_message(message)


    def process_message(self, message):
        is_spam = MessageRepository.spam_message_check(message)
        sleep(DELAY)
        if is_spam:
            MessageRepository.on_message_spam(message)
        else:
            MessageRepository.on_message_not_spam(message)


def main():
    subs_listener = MessagesListener()
    subs_listener.setDaemon(True)
    subs_listener.start()
    workers_count = 5
    for _ in range(workers_count):
        worker = MessageWorker()
        worker.daemon = True
        worker.start()
    while True:
        pass


if __name__ == '__main__':
    main()
