from db import red
from repositories.user import UserRepository

from models.msg_tag import Tag

from threading import Thread
from faker import Faker
from random import randint, choice

quantity_of_users = 20


class Emulation(Thread):
    def __init__(self, name, users):
        Thread.__init__(self)
        self.name = name
        self.users = users
        self.user_id = UserRepository.register(name)

    def get_tags(self) -> list:
        tags = set()
        for _ in range(3):
            tag = choice(list(Tag)).name
            tags.add(tag)
        return list(tags)

    def run(self):
        for _ in range(5):
            text = fake.sentence(nb_words=1, variable_nb_words=True, ext_word_list=None)
            recipient = users[randint(0, quantity_of_users - 1)]
            create_message(self.user_id, text, recipient, self.get_tags())


def run_seed():
    quantity_of_users = 3
    fake = Faker()
    users = [fake.profile(fields=["name"])["name"] for user in range(quantity_of_users)]
    threads = []

    for i in range(quantity_of_users):
        print(f"User: {users[i]}")
        threads.append(Emulation(users[i], users))

    for t in threads:
        t.start()

