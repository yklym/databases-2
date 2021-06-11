import os
import logging

LOG_FORMAT = "%%(levelname)s||(asctime)s====>%(message)s"


class Logger:
    def __init__(self):
        self.LOGS_FILENAME = os.path.join('./logs/logs.txt')
        logging.basicConfig(level='INFO', format=LOG_FORMAT, filename=self.LOGS_FILENAME)

    def login(self, username):
        logging.info(f'Login: {username}')


    def logout(self, username):
        logging.info(f'Logout: {username}')


    def spam(self, sender_name):
        logging.info(f'Spam: "{sender_name}"')


    def get_logs(self):
        try:
            with open(self.LOGS_FILENAME) as f:
                return f.read()
        except Exception:
            return "ERROR GETTING LOGS"

loggerService = Logger()