from random import choice, getrandbits

from faker import Faker

from db.redis_connection import r
from repositories.message import MessageRepository
from repositories.user import UserRepository

MOCKS_AMOUNT = 20
MESSAGES_AMOUNT = 4


class Seeder:
    def __init__(self):
        self.faker = Faker()

    def seed_mocks(self):
        r.flushall()
        users = [self.faker.unique.first_name() for _ in range(MOCKS_AMOUNT)]
        messages = [
            (self.faker.sentence(nb_words=5) + ('spam' if bool(getrandbits(1)) else ''))
            for _ in range(MOCKS_AMOUNT)
        ]
        for user in users:
            UserRepository.register(user)

        for i in range(MOCKS_AMOUNT):
            for j in range(MESSAGES_AMOUNT):
                receiver = choice(users[0:i] + users[i + 1:])  # not include user i
                message = choice(messages)
                MessageRepository.send_message(message, users[i], receiver)


seederService = Seeder()
