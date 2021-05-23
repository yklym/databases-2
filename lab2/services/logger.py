import logging
import os
from pathlib import Path

FORMAT = "%(asctime)s::%(levelname)s::%(message)s"


class Logger:
    def __init__(self):
        self.LOGS_FILENAME = os.path.join(os.path.dirname(Path(__file__).absolute()), '../logs/logs.txt')
        logging.basicConfig(level='INFO', format=FORMAT, filename=self.LOGS_FILENAME)


    def login(self, username):
        logging.info(f'LOGIN: {username}')


    def logout(self, username):
        logging.info(f'LOGOUT: {username}')


    def spam(self, sender_name):
        logging.info(f'SPAM from "{sender_name}"')


    def get_logs(self):
        try:
            with open(self.LOGS_FILENAME) as f:
                return f.read()
        except Exception:
            return "ERROR GETTING LOGS"

loggerService = Logger()